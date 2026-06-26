import { useMemo } from 'react';
import { billingOptions, plans } from '../data/pricingMatrix';
import { calculatePrice } from '../utils/calculatePrice';
import { formatCurrency } from '../utils/formatCurrency';

export function usePricing(billingCycle, currency) {
  return useMemo(() => {
    return plans.map((plan) => {
      const amount = calculatePrice(plan.key, billingCycle, currency);
      return {
        ...plan,
        amount,
        displayPrice: formatCurrency(amount, currency),
      };
    });
  }, [billingCycle, currency]);
}

export { billingOptions };