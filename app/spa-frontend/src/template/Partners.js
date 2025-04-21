import React, { useRef, useEffect } from 'react';
import '../styles/Partners.css'; 

function Partners() {
  const partnerLogos = [
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
    'https://array.com/_app/immutable/assets/array-logo-74cfaf49.svg',
  ];

  const scrollContainerRef = useRef(null);

  useEffect(() => {
    const scrollContainer = scrollContainerRef.current;
    const scrollInterval = setInterval(() => {
      if (scrollContainer) {
        scrollContainer.scrollLeft += 1;
        if (
          scrollContainer.scrollLeft + scrollContainer.clientWidth >=
          scrollContainer.scrollWidth
        ) {
          scrollContainer.scrollLeft = 0;
        }
      }
    }, 20); 

    return () => clearInterval(scrollInterval);
  }, []);

  return (
    <section className="partners">
      <h2>Our Partners</h2>
      <div className="partners-scroll" ref={scrollContainerRef}>
        {partnerLogos.map((logo, index) => (
          <div key={index} className="partner-item">
            <img src={logo} alt={`Partner ${index}`} />
          </div>
        ))}
      </div>
    </section>
  );
}

export default Partners;
