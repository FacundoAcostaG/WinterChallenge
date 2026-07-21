import { expect, test } from '@playwright/test';

import { MealDbClient } from '../clients/mealdb.client';
import { OpenMeteoClient } from '../clients/openmeteo.client';
import { WINTER_CHALLENGE_DATASET } from '../../shared/data/dynamic-test-set';
import { isWinterDishOfficiallyJustified } from '../../shared/utils/business-rules';
import {
  assertCityGeocodingShape,
  assertCurrentWeatherShape,
  assertMealDetailShape,
  assertMealSummaryShape
} from '../../shared/utils/validators';

test.describe('Winter Challenge - API tests', () => {
  test('TheMealDB: debería devolver resultados válidos al buscar "stew"', async ({ request }) => {
    // Creo el cliente para encapsular las llamadas a TheMealDB.
    const client = new MealDbClient(request);

    // Busco comidas por nombre usando el término "stew".
    const response = await client.searchMealsByName('stew');
    const body = await response.json();

    // Verifico que la API responda correctamente y con al menos un resultado.
    expect(response.status()).toBe(200);
    expect(Array.isArray(body.meals)).toBeTruthy();
    expect(body.meals.length).toBeGreaterThan(0);

    // Valido la estructura completa del primer resultado.
    assertMealDetailShape(body.meals[0]);
  });

  test('TheMealDB: debería devolver una lista resumida válida al filtrar por categoría Beef', async ({ request }) => {
    // Reutilizo el cliente de TheMealDB.
    const client = new MealDbClient(request);

    // Filtro comidas por categoría.
    const response = await client.filterByCategory('Beef');
    const body = await response.json();

    // Verifico que la consulta sea exitosa y devuelva datos.
    expect(response.status()).toBe(200);
    expect(Array.isArray(body.meals)).toBeTruthy();
    expect(body.meals.length).toBeGreaterThan(0);

    // En este caso valido la versión resumida del objeto meal.
    assertMealSummaryShape(body.meals[0]);
  });

  test('Open-Meteo: debería geolocalizar Montevideo correctamente', async ({ request }) => {
    // Creo el cliente para consultar Open-Meteo.
    const client = new OpenMeteoClient(request);

    // Busco Montevideo para obtener sus coordenadas.
    const response = await client.searchCityCoordinates('Montevideo');
    const body = await response.json();

    // Verifico que haya resultados válidos.
    expect(response.status()).toBe(200);
    expect(Array.isArray(body.results)).toBeTruthy();
    expect(body.results.length).toBeGreaterThan(0);

    // Valido la estructura del resultado geográfico.
    assertCityGeocodingShape(body.results[0]);
  });

  test('Open-Meteo: debería devolver clima actual con temperatura y lluvia', async ({ request }) => {
    // Este test usa dos pasos: geocoding primero, forecast después.
    const client = new OpenMeteoClient(request);

    // Primero busco la ciudad para conseguir latitud y longitud.
    const geocodingResponse = await client.searchCityCoordinates('Montevideo');
    const geocodingBody = await geocodingResponse.json();
    const [city] = geocodingBody.results;

    // Con esas coordenadas pido el clima actual.
    const weatherResponse = await client.getCurrentWeather(city.latitude, city.longitude);
    const weatherBody = await weatherResponse.json();

    // Valido que la respuesta tenga el formato esperado.
    expect(weatherResponse.status()).toBe(200);
    assertCurrentWeatherShape(weatherBody);
  });

  test('TheMealDB: debería devolver meals = null para un ID inexistente', async ({ request }) => {
    // Caso negativo: consulto por un ID que no debería existir.
    const client = new MealDbClient(request);

    const response = await client.lookupMealById('99999999');
    const body = await response.json();

    // La API responde 200, pero sin datos.
    expect(response.status()).toBe(200);
    expect(body.meals).toBeNull();
  });

  test('TheMealDB: debería devolver el mensaje "Invalid ID" para un ID con formato inválido', async ({ request }) => {
    // Caso negativo: el formato del ID es incorrecto.
    const client = new MealDbClient(request);

    const response = await client.lookupMealById('abc-invalid-id');
    const body = await response.json();

    // En este escenario TheMealDB devuelve el texto "Invalid ID".
    expect(response.status()).toBe(200);
    expect(body.meals).toBe('Invalid ID');
  });

  test('Open-Meteo: debería no devolver resultados para una ciudad inexistente', async ({ request }) => {
    // Caso negativo con una ciudad inventada.
    const client = new OpenMeteoClient(request);

    const response = await client.searchCityCoordinates('Paysandoom');
    const body = await response.json();

    // La API responde bien, pero sin coincidencias.
    expect(response.status()).toBe(200);
    expect(body.results ?? []).toHaveLength(0);
  });

  test('Integración: si la temperatura es menor a 15°C, el guiso queda oficialmente justificado', async ({ request }) => {
    // Este test integra ambas APIs y aplica la regla de negocio del challenge.
    const mealDbClient = new MealDbClient(request);
    const openMeteoClient = new OpenMeteoClient(request);

    // 1) Obtengo una comida desde TheMealDB.
    const mealResponse = await mealDbClient.filterByCategory('Beef');
    const mealBody = await mealResponse.json();

    expect(mealResponse.status()).toBe(200);
    expect(Array.isArray(mealBody.meals)).toBeTruthy();
    expect(mealBody.meals.length).toBeGreaterThan(0);

    const selectedMeal = mealBody.meals[0];

    // 2) Busco Montevideo para conseguir coordenadas reales.
    const cityResponse = await openMeteoClient.searchCityCoordinates('Montevideo');
    const cityBody = await cityResponse.json();
    const [city] = cityBody.results;

    expect(cityResponse.status()).toBe(200);
    expect(city).toBeTruthy();

    // 3) Consulto el clima actual con esas coordenadas.
    const weatherResponse = await openMeteoClient.getCurrentWeather(city.latitude, city.longitude);
    const weatherBody = await weatherResponse.json();

    expect(weatherResponse.status()).toBe(200);

    // 4) Tomo la temperatura actual devuelta por la API.
    const currentTemperature = weatherBody.current.temperature_2m;

    // 5) Aplico la regla del negocio: si hace menos de 15°C, el guiso se justifica.
    const justified = isWinterDishOfficiallyJustified(currentTemperature);

    // Verifico que tengo una comida válida y una temperatura numérica.
    expect(typeof selectedMeal.strMeal).toBe('string');
    expect(typeof currentTemperature).toBe('number');

    // Assert final del caso de negocio.
    expect(justified).toBe(true);
  });

  for (const scenario of WINTER_CHALLENGE_DATASET) {
    test(`Dataset dinámico: categoría ${scenario.mealCategory} con ciudad ${scenario.city}`, async ({ request }) => {
      // Este bloque repite la misma validación con varios datos de entrada.
      // Sirve para cumplir la parte del PDF que pide al menos 5 entradas dinámicas.
      const mealDbClient = new MealDbClient(request);
      const openMeteoClient = new OpenMeteoClient(request);

      // Valido que exista al menos una comida para la categoría elegida.
      const mealsResponse = await mealDbClient.filterByCategory(scenario.mealCategory);
      const mealsBody = await mealsResponse.json();

      expect(mealsResponse.status()).toBe(200);
      expect(Array.isArray(mealsBody.meals)).toBeTruthy();
      expect(mealsBody.meals.length).toBeGreaterThan(0);

      assertMealSummaryShape(mealsBody.meals[0]);

      // Valido que la ciudad del escenario exista en Open-Meteo.
      const cityResponse = await openMeteoClient.searchCityCoordinates(scenario.city);
      const cityBody = await cityResponse.json();

      expect(cityResponse.status()).toBe(200);
      expect(Array.isArray(cityBody.results)).toBeTruthy();
      expect(cityBody.results.length).toBeGreaterThan(0);
    });
  }
});
