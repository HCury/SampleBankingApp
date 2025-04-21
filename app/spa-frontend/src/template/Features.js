import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowForward } from '@mui/icons-material';
import '../styles/Features.css';

function Features() {
    const navigate = useNavigate();

    return (
        <section className="features">
            <div className="features-content">
                <h2>Revolutionizing Digital Banking</h2>
                <p>
                    Experience the future of banking with Bank of Henrique where security, convenience, and innovation come together.
                    Our platform offers seamless transactions, AI-driven fraud protection, and real-time financial management
                    to keep your money secure and accessible anytime, anywhere.
                </p>

                {/* Features Grid */}
                <div className="features-grid">
                    <div className="feature-card">
                        <h3>🔒 Bank-Grade Security</h3>
                        <p>Our end-to-end encryption and AI-driven fraud detection keep your funds and personal information safe.</p>
                    </div>
                    <div className="feature-card">
                        <h3>💳 Instant Transfers</h3>
                        <p>Send and receive money instantly with real-time transaction processing and zero hidden fees.</p>
                    </div>
                    <div className="feature-card">
                        <h3>📈 Smart Financial Insights</h3>
                        <p>AI-powered analytics help you track spending, optimize savings, and achieve your financial goals faster.</p>
                    </div>
                </div>
            </div>

            {/* Why Choose Us Section */}
            <div className="why-choose-us">
                <h2>Why Choose Us?</h2>

                {/* Card 1: Advanced Security */}
                <div className="choose-card">
                    <img
                        src="https://cdn.prod.website-files.com/637b540a6d55b65cfebb935c/637b540a6d55b6f1cfbb9398_Group%20550.svg"
                        alt="Advanced Security"
                    />
                    <div className="choose-content">
                        <h3>Advanced Security</h3>
                        <p>
                            Uncompromising Security for Your Financial Peace of Mind

                            At Bank of Henrique, we don't just secure your money; we secure your trust. Our advanced security measures are designed to provide you with the ultimate peace of mind in today's digital world.

                            Ironclad Encryption: Your data is protected by the strongest encryption standards, ensuring complete confidentiality.
                            Advanced Authentication: Multi-factor and biometric authentication options provide unparalleled security against unauthorized access.
                            Intelligent Fraud Protection: Our AI-powered systems detect and prevent fraud in real time, safeguarding your assets.
                            Your security is our unwavering commitment. Bank with confidence.
                        </p>
                    </div>
                </div>

                {/* Card 2: Seamless Experience */}
                <div className="choose-card">
                    <img
                        src="https://cdn.prod.website-files.com/637b540a6d55b65cfebb935c/637b540a6d55b6c4e5bb9394_Group%20547.svg"
                        alt="Seamless Experience"
                    />
                    <div className="choose-content">
                        <h3>Seamless User Experience</h3>
                        <p>
                            At Bank of Henrique, we redefine digital banking with an intuitive, user-friendly interface designed for effortless navigation.
                            Whether you're managing everyday transactions, setting up automatic bill payments, or tracking your financial growth, our platform ensures a smooth, hassle-free experience for users of all backgrounds.

                            Effortless Navigation: Our app features a clean, clutter-free design with easy-to-access menus and real-time updates making financial management more convenient than ever.
                            One-Tap Transfers: Instantly send or receive money with zero delays—whether you're splitting a bill, paying rent, or handling business transactions.
                            Personalized Dashboards: Get a comprehensive financial overview with AI-powered analytics, helping you track expenses, savings, and investments at a glance.
                            Smart Alerts & Notifications: Stay informed with real-time balance updates, security alerts, and transaction reminders to keep your finances on track.
                            24/7 Customer Support: Need help? Our dedicated support team is available round the clock, ensuring you receive the best assistance whenever needed.

                            With Bank of Henrique banking isn't just a necessity—it's a seamless experience designed to put control, security, and convenience at your fingertips.
                        </p>
                    </div>
                </div>

                {/* Card 3: Trusted by Thousands */}
                <div className="choose-card">
                    <img
                        src="https://cdn.prod.website-files.com/637b540a6d55b65cfebb935c/6659a6595d5b979e9a752272_map-illustration.webp"
                        alt="Trusted by Thousands"
                    />
                    <div className="choose-content">
                        <h3>Trusted by Thousands</h3>
                        <p>
                            At Bank of Henrique, we take pride in serving a growing community of individuals and businesses who rely on our secure and efficient banking solutions every day.
                            Whether you're a freelancer managing payments, a business owner handling payroll, or an individual tracking expenses, our platform ensures a safe, seamless, and highly reliable financial experience.

                            Widespread Adoption: With thousands of active users, our banking system is built to support both personal and business transactions with speed, accuracy, and security at its core.
                            Unmatched Security: Our users trust us because we implement bank-grade encryption, multi-factor authentication (MFA), and AI-driven fraud detection to keep their funds and data safe.
                            Business-Ready: From automated payroll solutions to instant invoicing and vendor payments, businesses of all sizes depend on our platform to streamline financial operations.
                            Financial Insights & Budgeting Tools: Our AI-powered analytics provide real-time insights, allowing users to make smarter financial decisions based on detailed expense tracking, savings goals, and customized reports.
                        </p>
                    </div>
                </div>
            </div>

            {/* Second Row: Single Password (Sign Up Card) */}
            <div className="trust-card trust-card--info">
                <p>
                    With Bank of Henrique, you get $1000 on sign up <strong>safely accessible in one place.</strong>
                </p>
                <button
                    className="btn btn-primary"
                    onClick={() => navigate('/signup')}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '10px 16px',
                        fontSize: '16px',
                        fontWeight: 'bold',
                    }}
                >
                    Sign up Now!
                    <ArrowForward />
                </button>
            </div>
        </section>
    );
}

export default Features;