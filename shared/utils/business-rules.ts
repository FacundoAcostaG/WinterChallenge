import { WINTER_RULES } from '../config/constants';

export function isWinterDishOfficiallyJustified(temperature: number): boolean {
  return temperature < WINTER_RULES.maxTemperatureForStewJustification;
}

