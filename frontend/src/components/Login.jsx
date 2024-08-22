import { useState, useEffect } from "react";
import axios from "axios";
// import { useAppDispatch } from "../app/store";
// import { login } from "../features/authentication/AuthenticationSlice";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

import "../css/Login.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const user = localStorage.getItem("user");
  const navigate = useNavigate();

  useEffect(() => {
    if (user?.token) {
      navigate("/dashboard");
    } else {
      navigate("/");
    }
  }, [user, navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();

    // Perform authentication logic here (e.g., send credentials to a server)
    try {
      // Example: Send login request to the server
      const response = await axios.post(
        "http://127.0.0.1:5000/authentication/login",
        {
          email,
          password,
        }
      );

      if (response.status === 200) {
        const userData = response.data;
        console.log(userData);
        localStorage.setItem("user", JSON.stringify(userData));
        navigate("/build");
      } else {
        console.error("Login failed");
      }
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  return (
    <div className="login-page-container">
      <div className="login-page">
        <div className="register-page-logo-organisation">
          <p>ResumeSmart</p>
        </div>
        <h2>Welcome Back !</h2>
        <p>Register to unlock the benefits of daily calorie tracking</p>
        <form onSubmit={handleLogin} className="login-form">
          <div>
            <label>Email:</label>
            <input
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
            />
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
            />
          </div>
          <button type="submit">Log In</button>
        </form>
        <p className="register-link">
          Dont have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
