import { testimonials } from '../../data/testimonials';

export default function Testimonials() {
  return (
    <section className="section" id="testimonials" aria-labelledby="testimonials-title">
      <div className="container">
        <div className="section-heading">
          <span className="kicker">Social proof</span>
          <h2 id="testimonials-title" className="section-title">
            Teams use AstraFlow to reduce manual work and improve data trust.
          </h2>
        </div>

        <div className="testimonial-grid">
          {testimonials.map((testimonial) => (
            <figure key={testimonial.name} className="testimonial card">
              <blockquote>{testimonial.quote}</blockquote>
              <figcaption>
                <strong>{testimonial.name}</strong>
                <span>{testimonial.role}</span>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}