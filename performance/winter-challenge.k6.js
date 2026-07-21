import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';

// Ciudades válidas pedidas.
const VALID_CITIES = [
  'Montevideo',
  'Salto',
  'Paysandu',
  'Las Piedras',
  'Rivera',
  'Maldonado',
  'Tacuarembo'
];

// Errores simulados.
const INVALID_CITIES = [
  'Montefideo',
  'Paysandoom',
  'Tacuaremboom',
  'Maldolado'
];

const GEOCODING_BASE_URL = 'https://geocoding-api.open-meteo.com/v1/search';
const FORECAST_BASE_URL = 'https://api.open-meteo.com/v1/forecast';

// Métricas custom para complementar las métricas nativas de k6.
const apiErrorRate = new Rate('api_error_rate');
const invalidCityHandledRate = new Rate('invalid_city_handled_rate');
const productionAlertCounter = new Counter('production_alert_200_count');
const crocanciaIndexTrend = new Trend('crocancia_index');

export const options = {
  scenarios: {
    // 80 usuarios concurrentes consultando ciudades válidas.
    valid_cities_load: {
      executor: 'constant-vus',
      exec: 'validCitiesScenario',
      vus: 80,
      duration: '2m'
    },
    // 20 usuarios concurrentes generando errores simulados.
    invalid_cities_load: {
      executor: 'constant-vus',
      exec: 'invalidCitiesScenario',
      vus: 20,
      duration: '2m'
    }
  },
  thresholds: {
    // Métricas relevantes del challenge.
    http_req_duration: ['avg<2000', 'p(95)<3500'],
    http_req_failed: ['rate<0.10'],
    api_error_rate: ['rate<0.10'],
    invalid_city_handled_rate: ['rate>0.90']
  }
};

function randomItem(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function buildGeocodingUrl(city) {
  return `${GEOCODING_BASE_URL}?name=${encodeURIComponent(city)}&count=1&language=en&format=json`;
}

function buildForecastUrl(latitude, longitude) {
  return `${FORECAST_BASE_URL}?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,rain&timezone=auto`;
}

function calculateCrocanciaIndex(temperature, rain) {
  // Más lluvia y más frío => más necesidad de torta frita => más "crocancia".
  const coldFactor = Math.max(0, 15 - temperature);
  const rainFactor = Math.max(0, rain) * 10;

  return Number((coldFactor + rainFactor).toFixed(2));
}

function isProductionAlertNeeded(temperature, rain) {
  return rain > 0 && temperature < 15;
}

export function validCitiesScenario() {
  const city = randomItem(VALID_CITIES);

  group(`valid city flow - ${city}`, () => {
    // 1) Busco coordenadas de la ciudad.
    const geocodingResponse = http.get(buildGeocodingUrl(city));

    const geocodingOk = check(geocodingResponse, {
      'geocoding status is 200': (response) => response.status === 200
    });

    apiErrorRate.add(!geocodingOk);

    const geocodingBody = geocodingResponse.json();
    const results = geocodingBody.results || [];

    const cityFound = check(geocodingBody, {
      'valid city returns at least one result': () => results.length > 0
    });

    apiErrorRate.add(!cityFound);

    if (!cityFound) {
      return;
    }

    const selectedCity = results[0];

    // 2) Con las coordenadas pido el clima actual.
    const forecastResponse = http.get(
      buildForecastUrl(selectedCity.latitude, selectedCity.longitude)
    );

    const forecastOk = check(forecastResponse, {
      'forecast status is 200': (response) => response.status === 200
    });

    apiErrorRate.add(!forecastOk);

    const forecastBody = forecastResponse.json();
    const current = forecastBody.current || {};

    const weatherPayloadOk = check(current, {
      'current temperature exists': (payload) => typeof payload.temperature_2m === 'number',
      'current rain exists': (payload) => typeof payload.rain === 'number'
    });

    apiErrorRate.add(!weatherPayloadOk);

    if (!weatherPayloadOk) {
      return;
    }

    // 3) Aplico la regla de negocio del challenge.
    const productionAlert = isProductionAlertNeeded(current.temperature_2m, current.rain);

    if (productionAlert) {
      productionAlertCounter.add(1);
    }

    // 4) Registro el bonus inventado de "índice de crocancia".
    crocanciaIndexTrend.add(
      calculateCrocanciaIndex(current.temperature_2m, current.rain)
    );
  });

  // Cada usuario virtual consulta cada 5 segundos.
  sleep(5);
}

export function invalidCitiesScenario() {
  const city = randomItem(INVALID_CITIES);

  group(`invalid city flow - ${city}`, () => {
    // Este escenario valida que el sistema tolere nombres mal escritos o inexistentes.
    const geocodingResponse = http.get(buildGeocodingUrl(city));

    const geocodingOk = check(geocodingResponse, {
      'invalid city geocoding status is 200': (response) => response.status === 200
    });

    apiErrorRate.add(!geocodingOk);

    const geocodingBody = geocodingResponse.json();
    const results = geocodingBody.results || [];

    const invalidCityHandled = check(geocodingBody, {
      'invalid city returns zero results': () => results.length === 0
    });

    invalidCityHandledRate.add(invalidCityHandled);
    apiErrorRate.add(!invalidCityHandled);
  });

  // Mantengo la misma frecuencia que en el escenario válido.
  sleep(5);
}
