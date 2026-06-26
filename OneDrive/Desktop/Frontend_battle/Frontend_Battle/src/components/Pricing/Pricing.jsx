import { useEffect, useRef } from 'react';
import { billingOptions, currencyMeta, plans } from '../../data/pricingMatrix';
import { calculatePrice } from '../../utils/calculatePrice';
import { formatCurrency } from '../../utils/formatCurrency';

export default function Pricing() {
  const controlsRef = useRef(null);
  const priceRefs = useRef({});
  const cycleRefs = useRef({});
  const stateRef = useRef({ billingCycle: 'monthly', currency: 'INR' });

    const syncPricing = () => {
      const { billingCycle, currency } = stateRef.current;
      plans.forEach((plan) => {
        const amount = calculatePrice(plan.key, billingCycle, currency);
        const node = priceRefs.current[plan.key];
        if (node) {
          node.textContent = formatCurrency(amount, currency, currencyMeta[currency].locale);
        }

        const cycleNode = cycleRefs.current[plan.key];
        if (cycleNode) {
          cycleNode.textContent = billingCycle === 'annual' ? 'per year' : 'per month';
        }
      });
    };

  useEffect(() => {

    const onChange = (event) => {
      const target = event.target;
      if (!(target instanceof HTMLElement)) return;

      if (target.matches('[data-billing]')) {
        stateRef.current.billingCycle = target.value;
      }

      if (target.matches('[data-currency]')) {
        stateRef.current.currency = target.value;
      }

      syncPricing();
    };

      syncPricing();
    const controls = controlsRef.current;
    controls?.addEventListener('change', onChange);
    return () => controls?.removeEventListener('change', onChange);
  }, []);

  return (
    <section className="section" id="pricing" aria-labelledby="pricing-title">
      <div className="container">
        <div className="section-heading pricing-heading">
          <span className="kicker">Pricing</span>
          <h2 id="pricing-title" className="section-title">
            Matrix-driven pricing with live billing and currency updates.
          </h2>
          <p className="section-copy">
            Pricing values are stored in a multidimensional configuration object, annual totals are derived dynamically, and only the targeted price nodes are updated on change.
          </p>
        </div>

        <div className="pricing-controls card" ref={controlsRef}>
          <fieldset>
            <legend>Billing cycle</legend>
            <div className="segmented-control" role="radiogroup" aria-label="Billing cycle">
              {billingOptions.map((option) => (
                <label key={option.key} className="segmented-option">
                  <input type="radio" name="billing" value={option.key} data-billing defaultChecked={option.key === 'monthly'} />
                  <span>
                    {option.label}
                    {option.suffix ? <small>{option.suffix}</small> : null}
                  </span>
                </label>
              ))}
            </div>
          </fieldset>

          <fieldset>
            <legend>Currency</legend>
            <div className="segmented-control segmented-select">
              <label className="currency-select">
                <span>Display currency</span>
                <select defaultValue="INR" data-currency aria-label="Currency selector">
                  {Object.keys(currencyMeta).map((currency) => (
                    <option key={currency} value={currency}>
                      {currency}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          </fieldset>
        </div>

        <div className="pricing-grid">
          {plans.map((plan) => (
            <article key={plan.key} className={`pricing-card card ${plan.key === 'pro' ? 'featured' : ''}`}>
              <div className="pricing-card-top">
                <span className="chip">{plan.badge}</span>
                <h3>{plan.name}</h3>
                <p>{plan.description}</p>
              </div>
              <div className="pricing-price">
                <strong ref={(node) => {
                  priceRefs.current[plan.key] = node;
                }} />
                <span ref={(node) => {
                  cycleRefs.current[plan.key] = node;
                }} className="pricing-cycle">
                  per month
                </span>
              </div>
              <ul>
                {plan.features.map((feature) => (
                  <li key={feature}>{feature}</li>
                ))}
              </ul>
              <a className="btn btn-secondary pricing-cta" href="#cta">
                Get started
              </a>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}