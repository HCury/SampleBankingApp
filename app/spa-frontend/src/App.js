import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Header from './template/Header';
import Footer from './template/Footer';
import HeroSection from './template/HeroSection';
import TrustSection from './template/TrustSection';
import Partners from './template/Partners';
import Login from './pages/Login';
import Signup from './pages/Signup';
import TransactionsPage from './pages/Transactions';
import { ThemeProvider } from '@emotion/react';
import theme from './theme';
import Features from './template/Features';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Routes>
          {/* Home Page (With Full Layout) */}
          <Route
            path="/"
            element={
              <>
                <Header />
                <HeroSection />
                <Partners />
                <TrustSection />
                <Features />
                <Footer />
              </>
            }
          />

          {/* Login Page (Standalone) */}
          <Route
            path="/login"
            element={
              <>
                <Header />
                <Login />
                <Footer />
              </>
            }
          />

          {/* Signup Page (Standalone) */}
          <Route
            path="/signup"
            element={
              <>
                <Header />
                <Signup />
                <Footer />
              </>
            }
          />

          {/* Transactions Page */}
          <Route
            path="/transactions"
            element={
              <>
                <Header />
                <TransactionsPage />
                <Footer />
              </>
            }
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
