import FeatureCard from './FeatureCard';

export default function BentoGrid({ features, activeKey, onActivate }) {
  return (
    <div className="bento-grid" role="list">
      {features.map((feature) => (
        <FeatureCard key={feature.key} feature={feature} active={activeKey === feature.key} onActivate={() => onActivate(feature.key)} />
      ))}
    </div>
  );
}