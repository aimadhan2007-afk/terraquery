export default function CTA() {
  return (
    <section className="section cta-section" id="cta" aria-labelledby="cta-title">
      <div className="container cta card">
        <div>
          <span className="kicker">Ready to scale</span>
          <h2 id="cta-title" className="section-title">
            Launch an automation stack your team can trust.
          </h2>
          <p className="section-copy">
            Start with a guided trial, validate your highest-friction workflows, and expand with confidence.
          </p>
        </div>
        <div className="cta-actions">
          <a className="btn btn-primary" href="#pricing">
            Start free trial
          </a>
          <a className="btn btn-secondary" href="mailto:hello@astraflow.ai">
            Talk to sales
          </a>
        </div>
      </div>
    </section>
  );
}