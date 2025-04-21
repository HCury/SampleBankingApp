import React from 'react';
import '../styles/TrustSection.css';

function TrustSection() {
    return (
        <section className="trust-section">
            <div className="trust-container">
                {/* Left: Secure Banking Card */}
                <div className="trust-card trust-card--highlight">
                    <div className="trust-text">
                        <h2>Secure Banking &amp; Build Trust</h2>
                        <p>
                            Our advanced banking solutions ensure secure transactions, fraud prevention,
                            and seamless financial management. With cutting-edge encryption and AI-powered
                            security, we protect your personal and financial data while providing a seamless
                            banking experience. Whether you're making payments, managing investments, or
                            applying for loans, your trust is our priority.
                        </p>
                    </div>
                    <div className="trust-illustration">
                        <img
                            src="https://img.icons8.com/nolan/64/bank-building.png"
                            alt="Illustration: ID Fraud Prevention"
                        />
                    </div>
                </div>

                {/* Right: Seamless Digital Banking Solutions */}
                <div className="trust-card trust-card--side"> 
                    <h2>Seamless Digital Banking Solutions</h2>
                    <p>
                        We leverage advanced financial technology to enhance security, streamline transactions,
                        and provide a seamless banking experience. Our platform ensures secure digital identity
                        verification, real-time fraud protection, and easy access to financial services.
                        Whether you're managing personal accounts or business finances, our innovative banking
                        solutions are designed to keep your money safe and accessible.
                    </p>
                </div>
            </div>
        </section>
    );
}

export default TrustSection;