export interface MealSummary {
  idMeal: string;
  strMeal: string;
  strMealThumb: string;
}

export interface MealDetail extends MealSummary {
  strCategory: string;
  strArea: string;
  strInstructions: string;
}

export interface CityGeocodingResult {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  country?: string;
}

export interface CurrentWeatherPayload {
  latitude: number;
  longitude: number;
  current: {
    time: string;
    interval?: number;
    temperature_2m: number;
    rain?: number;
  };
}

