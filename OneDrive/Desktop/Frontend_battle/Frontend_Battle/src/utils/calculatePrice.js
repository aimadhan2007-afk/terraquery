import { pricingMatrix } from '../data/pricingMatrix';

export function calculatePrice(planKey, billingCycle, currency) {
  const basePrice = pricingMatrix.monthly[planKey][currency];
  if (billingCycle === 'annual') {
    return Math.round(basePrice * 12 * 0.8);
  }
  return basePrice;
}