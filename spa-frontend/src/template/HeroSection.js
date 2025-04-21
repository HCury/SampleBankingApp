import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/HeroSection.css';

function HeroSection() {
  const navigate = useNavigate(); 

  return (
    <section className="hero">
      <div className="hero-content">
        <h1>Your Bank Just Got an Upgrade</h1>
        <h2>Seamless Digital Banking &amp; Fraud Protection</h2>
        <p>
          Manage your finances securely and easily with real-time transaction
          alerts, automated savings, and advanced fraud detection. Whether you're
          making payments, applying for loans, or managing investments, we've got you covered.
        </p>
        <div className="hero-buttons">
          <button className="btn btn-primary" onClick={() => navigate('/login')}>
            Login
          </button>
          <button className="btn btn-outline" onClick={() => navigate('/signup')}>
            Sign Up
          </button>
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
