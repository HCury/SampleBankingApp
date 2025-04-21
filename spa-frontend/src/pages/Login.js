import React, { useState } from 'react';
import '../styles/Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString(),
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        window.location.href = '/transactions'; 
      } else {
        alert(data.detail || data.message || 'Login Failed');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Something went wrong: ' + error);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-content">
        <div className="auth-container">
          <h2>Login to Your Account</h2>
          <form onSubmit={handleSubmit}>
            <input 
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)} 
              required
            />
            <input 
              type="password" 
              placeholder="Password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required
            />
            <button type="submit" className="btn btn-primary">Login</button>
          </form>
          <p>Don't have an account? <a href="/signup">Sign Up</a></p>
        </div>
      </div>
    </div>
  );
}

export default Login;
