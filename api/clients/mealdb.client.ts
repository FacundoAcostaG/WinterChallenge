import type { APIRequestContext, APIResponse } from '@playwright/test';

import { API_ENDPOINTS } from '../../shared/config/endpoints';

export class MealDbClient {
  constructor(private readonly request: APIRequestContext) {}

  searchMealsByName(searchTerm: string): Promise<APIResponse> {
    return this.request.get(`${API_ENDPOINTS.mealDbBaseUrl}/search.php`, {
      params: { s: searchTerm }
    });
  }

  lookupMealById(mealId: string): Promise<APIResponse> {
    return this.request.get(`${API_ENDPOINTS.mealDbBaseUrl}/lookup.php`, {
      params: { i: mealId }
    });
  }

  filterByCategory(category: string): Promise<APIResponse> {
    return this.request.get(`${API_ENDPOINTS.mealDbBaseUrl}/filter.php`, {
      params: { c: category }
    });
  }
}

