import type { APIRequestContext, APIResponse } from '@playwright/test';

import { API_ENDPOINTS } from '../../shared/config/endpoints';

export class OpenMeteoClient {
  constructor(private readonly request: APIRequestContext) {}

  searchCityCoordinates(city: string): Promise<APIResponse> {
    return this.request.get(`${API_ENDPOINTS.openMeteoGeocodingBaseUrl}/search`, {
      params: {
        name: city,
        count: 1,
        language: 'en',
        format: 'json'
      }
    });
  }

  getCurrentWeather(latitude: number, longitude: number): Promise<APIResponse> {
    return this.request.get(`${API_ENDPOINTS.openMeteoForecastBaseUrl}/forecast`, {
      params: {
        latitude,
        longitude,
        current: 'temperature_2m,rain',
        timezone: 'auto'
      }
    });
  }
}

