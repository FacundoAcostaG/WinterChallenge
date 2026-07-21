import { expect } from '@playwright/test';

import type {
  CityGeocodingResult,
  CurrentWeatherPayload,
  MealDetail,
  MealSummary
} from '../types/api.types';

function expectNonEmptyString(value: unknown, fieldName: string): void {
  expect(typeof value, `${fieldName} should be a string`).toBe('string');
  expect((value as string).trim().length, `${fieldName} should not be empty`).toBeGreaterThan(0);
}

function expectNumber(value: unknown, fieldName: string): void {
  expect(typeof value, `${fieldName} should be a number`).toBe('number');
  expect(Number.isFinite(value), `${fieldName} should be finite`).toBeTruthy();
}

export function assertMealSummaryShape(meal: MealSummary): void {
  expect(meal).toBeTruthy();
  expectNonEmptyString(meal.idMeal, 'idMeal');
  expectNonEmptyString(meal.strMeal, 'strMeal');
  expectNonEmptyString(meal.strMealThumb, 'strMealThumb');
}

export function assertMealDetailShape(meal: MealDetail): void {
  assertMealSummaryShape(meal);
  expectNonEmptyString(meal.strCategory, 'strCategory');
  expectNonEmptyString(meal.strArea, 'strArea');
  expectNonEmptyString(meal.strInstructions, 'strInstructions');
}

export function assertCityGeocodingShape(city: CityGeocodingResult): void {
  expect(city).toBeTruthy();
  expectNumber(city.id, 'id');
  expectNonEmptyString(city.name, 'name');
  expectNumber(city.latitude, 'latitude');
  expectNumber(city.longitude, 'longitude');
}

export function assertCurrentWeatherShape(payload: CurrentWeatherPayload): void {
  expect(payload).toBeTruthy();
  expectNumber(payload.latitude, 'latitude');
  expectNumber(payload.longitude, 'longitude');
  expect(payload.current).toBeTruthy();
  expectNonEmptyString(payload.current.time, 'current.time');
  expectNumber(payload.current.temperature_2m, 'current.temperature_2m');

  if (payload.current.rain !== undefined) {
    expectNumber(payload.current.rain, 'current.rain');
  }
}
