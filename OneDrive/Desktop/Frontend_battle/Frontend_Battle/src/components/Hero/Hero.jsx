export default function Hero() {
  return (
    <section className="hero section" id="top">
      <div className="container hero-grid reveal">
        <div className="hero-copy">
          <span className="kicker">AI-powered data automation</span>
          <h1>Automate data workflows with precision, speed, and measurable ROI.</h1>
          <p>
            Orchestrate extraction, enrichment, routing, and reporting in one premium SaaS platform designed for modern growth and operations teams.
          </p>
          <div className="hero-actions">
            <a className="btn btn-primary" href="#pricing">
              Start free trial
            </a>
            <a className="btn btn-secondary" href="#features">
              Explore features
            </a>
          </div>
          <div className="hero-stats" aria-label="Platform stats">
            <div>
              <strong>85%</strong>
              <span>less manual work</span>
            </div>
            <div>
              <strong>140ms</strong>
              <span>median automation latency</span>
            </div>
            <div>
              <strong>99.9%</strong>
              <span>workflow uptime target</span>
            </div>
          </div>
        </div>

        <div className="hero-visual card" aria-hidden="true">
          <div className="hero-orb hero-orb-one" />
          <div className="hero-orb hero-orb-two" />
          <div className="hero-dashboard">
            <div className="hero-dashboard-top">
              <span>Pipeline health</span>
              <span className="chip">Live</span>
            </div>
            <div className="hero-dashboard-chart">
              <span />
              <span />
              <span />
              <span />
              <span />
            </div>
            <div className="hero-dashboard-grid">
              <article>
                <small>Inbound records</small>
                <strong>12.4M</strong>
              </article>
              <article>
                <small>Auto-resolved</small>
                <strong>97.2%</strong>
              </article>
              <article>
                <small>Saved hours</small>
                <strong>1,248</strong>
              </article>
              <article>
                <small>Policy checks</small>
                <strong>Zero drift</strong>
              </article>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}