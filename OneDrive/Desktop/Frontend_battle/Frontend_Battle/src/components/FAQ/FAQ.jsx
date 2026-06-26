import { useState } from 'react';
import { faqItems } from '../../data/faq';

export default function FAQ() {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <section className="section" id="faq" aria-labelledby="faq-title">
      <div className="container">
        <div className="section-heading">
          <span className="kicker">FAQ</span>
          <h2 id="faq-title" className="section-title">
            Clear answers for teams evaluating enterprise automation.
          </h2>
        </div>

        <div className="faq-list">
          {faqItems.map((item, index) => {
            const open = activeIndex === index;
            return (
              <article key={item.question} className={`faq-item card ${open ? 'open' : ''}`}>
                <button type="button" className="faq-trigger" aria-expanded={open} onClick={() => setActiveIndex(open ? -1 : index)}>
                  <span>{item.question}</span>
                  <span aria-hidden="true">{open ? '−' : '+'}</span>
                </button>
                <div className="faq-panel" hidden={!open}>
                  <p>{item.answer}</p>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}