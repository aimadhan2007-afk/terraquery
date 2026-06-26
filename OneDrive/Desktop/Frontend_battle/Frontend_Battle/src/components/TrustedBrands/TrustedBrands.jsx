const brands = ['Northstar', 'Vertex', 'Helix', 'Orbit', 'Foundry', 'Lattice'];

export default function TrustedBrands() {
  return (
    <section className="section trusted" aria-labelledby="trusted-title">
      <div className="container">
        <p id="trusted-title" className="trusted-label">
          Trusted by teams that automate at scale
        </p>
        <div className="trusted-strip card">
          {brands.map((brand) => (
            <span key={brand}>{brand}</span>
          ))}
        </div>
      </div>
    </section>
  );
}