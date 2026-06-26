import { useEffect, useMemo, useState } from 'react';
import { useBreakpoint } from '../../hooks/useBreakpoint';
import BentoGrid from './BentoGrid';
import Accordion from './Accordion';

const featureEntries = [
  { key: 'orchestration', title: 'Autonomous orchestration', description: 'Route records through workflows that adapt in real time.', points: ['Visual flow builder', 'Event and batch triggers', 'Retry-aware execution'] },
  { key: 'enrichment', title: 'AI enrichment engine', description: 'Classify and enrich structured and unstructured data.', points: ['Entity recognition', 'Normalization rules', 'Confidence scoring'] },
  { key: 'observability', title: 'Operational observability', description: 'See workflow health, drift, and throughput instantly.', points: ['Audit logs', 'Anomaly detection', 'Executive dashboards'] },
  { key: 'security', title: 'Governed integration fabric', description: 'Connect the stack with policy-first controls.', points: ['Role-aware access', 'Private deployments', 'Connector library'] },
  { key: 'analytics', title: 'Outcome intelligence', description: 'Measure cost savings and productivity gains.', points: ['ROI tracking', 'Forecasting', 'Export-ready reports'] },
  { key: 'scheduling', title: 'Adaptive scheduling', description: 'Balance recurring, event-driven, and queue-based work.', points: ['Time windows', 'Load balancing', 'Alert routing'] },
];

export default function Features() {
  const isDesktop = useBreakpoint('(min-width: 960px)');
  const [activeKey, setActiveKey] = useState(featureEntries[0].key);

  useEffect(() => {
    setActiveKey((current) => current || featureEntries[0].key);
  }, [isDesktop]);

  const activeFeature = useMemo(() => featureEntries.find((feature) => feature.key === activeKey) || featureEntries[0], [activeKey]);

  return (
    <section className="section" id="features" aria-labelledby="features-title">
      <div className="container">
        <div className="section-heading">
          <span className="kicker">Features</span>
          <h2 id="features-title" className="section-title">
            Bento on desktop. Accordion on mobile. Same context everywhere.
          </h2>
          <p className="section-copy">
            The feature experience remains continuous across viewport changes, preserving the active card or panel without losing user context.
          </p>
        </div>

        <div className="features-layout card">
          <div className="feature-summary">
            <span className="chip">Context lock active</span>
            <h3>{activeFeature.title}</h3>
            <p>{activeFeature.description}</p>
          </div>

          {isDesktop ? (
            <BentoGrid features={featureEntries} activeKey={activeKey} onActivate={setActiveKey} />
          ) : (
            <Accordion features={featureEntries} activeKey={activeKey} onToggle={setActiveKey} />
          )}
        </div>
      </div>
    </section>
  );
}