export default function FeatureCard({ feature, active, onActivate }) {
  return (
    <button className={`feature-card ${active ? 'active' : ''}`} type="button" onClick={onActivate} aria-pressed={active}>
      <span className="feature-icon" aria-hidden="true" />
      <span className="feature-card-text">
        <strong>{feature.title}</strong>
        <span>{feature.description}</span>
      </span>
    </button>
  );
}