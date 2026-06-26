import { useState } from 'react';

const navItems = [
  ['Features', '#features'],
  ['Pricing', '#pricing'],
  ['Testimonials', '#testimonials'],
  ['FAQ', '#faq'],
];

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="site-header">
      <div className="container nav-shell">
        <a className="brand" href="#top" aria-label="AstraFlow AI home">
          <span className="brand-mark">AF</span>
          <span>
            <strong>AstraFlow AI</strong>
            <small>Data automation platform</small>
          </span>
        </a>

        <nav className="desktop-nav" aria-label="Primary">
          {navItems.map(([label, href]) => (
            <a key={label} href={href}>
              {label}
            </a>
          ))}
        </nav>

        <div className="nav-actions">
          <a className="btn btn-secondary nav-ghost" href="#pricing">
            View pricing
          </a>
          <button
            className="menu-toggle"
            type="button"
            aria-expanded={menuOpen}
            aria-controls="mobile-menu"
            onClick={() => setMenuOpen((value) => !value)}
          >
            Menu
          </button>
        </div>
      </div>

      <div id="mobile-menu" className={`mobile-panel ${menuOpen ? 'open' : ''}`}>
        <nav aria-label="Mobile">
          {navItems.map(([label, href]) => (
            <a key={label} href={href} onClick={() => setMenuOpen(false)}>
              {label}
            </a>
          ))}
          <a className="btn btn-primary mobile-cta" href="#pricing" onClick={() => setMenuOpen(false)}>
            Start free trial
          </a>
        </nav>
      </div>
    </header>
  );
}