export default function Accordion({ features, activeKey, onToggle }) {
  return (
    <div className="accordion" role="presentation">
      {features.map((feature) => {
        const open = activeKey === feature.key;
        const panelId = `feature-panel-${feature.key}`;
        const buttonId = `feature-button-${feature.key}`;

        return (
          <article key={feature.key} className={`accordion-item ${open ? 'open' : ''}`}>
            <h3 className="accordion-heading">
              <button
                id={buttonId}
                className="accordion-trigger"
                type="button"
                aria-expanded={open}
                aria-controls={panelId}
                onClick={() => onToggle(feature.key)}
              >
                <span>{feature.title}</span>
                <span aria-hidden="true">+</span>
              </button>
            </h3>
            <div id={panelId} className="accordion-panel" role="region" aria-labelledby={buttonId} hidden={!open}>
              <p>{feature.description}</p>
              <ul>
                {feature.points.map((point) => (
                  <li key={point}>{point}</li>
                ))}
              </ul>
            </div>
          </article>
        );
      })}
    </div>
  );
}