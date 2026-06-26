export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="container footer-grid">
        <div>
          <a className="brand footer-brand" href="#top">
            <span className="brand-mark">AF</span>
            <span>
              <strong>AstraFlow AI</strong>
              <small>Data automation platform</small>
            </span>
          </a>
          <p>
            Premium automation for operations, growth, and data teams.
          </p>
        </div>
        <div>
          <strong>Product</strong>
          <a href="#features">Features</a>
          <a href="#pricing">Pricing</a>
          <a href="#faq">FAQ</a>
        </div>
        <div>
          <strong>Company</strong>
          <a href="#testimonials">Customers</a>
          <a href="mailto:hello@astraflow.ai">Contact</a>
          <a href="#top">Back to top</a>
        </div>
      </div>
    </footer>
  );
}