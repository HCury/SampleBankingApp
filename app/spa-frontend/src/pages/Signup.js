import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Signup.css';

function Signup() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password', password);

    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData, 
      });

      const data = await response.json();
      if (response.ok) {
        alert('Signup Successful!');
        navigate('/login'); 
      } else {
        alert(data.detail || data.message || 'Signup Failed');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Something went wrong.' + error);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-content">
        <div className="auth-container">
          <h2>Create an Account</h2>
          <form onSubmit={handleSubmit}>
            <input 
              type="text"  
              placeholder="Username"  
              value={username}  
              onChange={(e) => setUsername(e.target.value)}  
              required
            />
            <input 
              type="email"  
              placeholder="Email"  
              value={email}  
              onChange={(e) => setEmail(e.target.value)}  
              required
            />
            <input 
              type="password"  
              placeholder="Password"  
              value={password}  
              onChange={(e) => setPassword(e.target.value)}  
              required
            />
            <button type="submit" className="btn btn-primary">Sign Up</button>
          </form>
          <p>Already have an account? <a href="/login">Login</a></p>
        </div>
      </div>
    </div>
  );
}

export default Signup;
