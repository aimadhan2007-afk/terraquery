export const pricingMatrix = {
  monthly: {
    basic: { INR: 1499, USD: 19, EUR: 18 },
    pro: { INR: 4999, USD: 59, EUR: 56 },
    enterprise: { INR: 15999, USD: 179, EUR: 169 },
  },
  annual: {
    basic: { INR: 1499, USD: 19, EUR: 18 },
    pro: { INR: 4999, USD: 59, EUR: 56 },
    enterprise: { INR: 15999, USD: 179, EUR: 169 },
  },
};

export const plans = [
  {
    key: 'basic',
    name: 'Basic',
    badge: 'Fast start',
    description: 'For lean teams automating high-volume manual work.',
    features: ['3 workflows', 'Email support', 'Core analytics'],
  },
  {
    key: 'pro',
    name: 'Pro',
    badge: 'Most popular',
    description: 'For growing teams orchestrating critical operations.',
    features: ['Unlimited workflows', 'Advanced integrations', 'Priority support'],
  },
  {
    key: 'enterprise',
    name: 'Enterprise',
    badge: 'Scale securely',
    description: 'For global organizations with governance and compliance needs.',
    features: ['Custom SLAs', 'Dedicated success manager', 'Private deployments'],
  },
];

export const currencyMeta = {
  INR: { symbol: '₹', locale: 'en-IN' },
  USD: { symbol: '$', locale: 'en-US' },
  EUR: { symbol: '€', locale: 'de-DE' },
};

export const billingOptions = [
  { key: 'monthly', label: 'Monthly' },
  { key: 'annual', label: 'Annual', suffix: 'Save 20%' },
];