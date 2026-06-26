import { currencyMeta } from '../data/pricingMatrix';

export function formatCurrency(value, currency, localeOverride) {
  const meta = currencyMeta[currency];
  return new Intl.NumberFormat(localeOverride || meta.locale, {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).format(value);
}