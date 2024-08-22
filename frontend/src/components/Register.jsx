import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

import "../css/Register.css";

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const user = localStorage.getItem("user");

  const navigate = useNavigate();
  useEffect(() => {
    if (user?.token) {
      navigate("/build");
    }
  }, [user, navigate]);

  const handleRegister = async (e) => {
    e.preventDefault();

    // Validate form data
    if (password !== confirmPassword) {
      console.error("Passwords do not match");
      // Handle error, show error message, etc.
      return;
    }

    // Perform registration logic here (e.g., send data to a server)
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/authentication/register",
        {
          name: name,
          email: email,
          password: password,
        }
      );

      if (response.status === 201) {
        const userData = response.data;
        localStorage.setItem("user", JSON.stringify(userData));
        navigate("/build");
      } else {
        console.error(
          "Registration failed. Server returned:",
          response.status,
          response.data
        );
      }
    } catch (error) {
      console.error("Error during registration:", error);
    }
  };

  return (
    <div className="register-page-container">
      <div className="register-page">
        <div className="register-page-logo-organisation">
          {/* <img src={calorific_logo} alt="" className="calorific_logo" /> */}
          <p>ResumeSmart</p>
        </div>
        <h2>Register</h2>
        <p>Register to unlock the benefits of daily calorie tracking</p>
        <form onSubmit={handleRegister} className="register-form">
          <div>
            <label>Name:</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
            />
          </div>
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
              placeholder="Enter password"
            />
          </div>
          <div>
            <label>Confirm Password:</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Re-enter the password"
            />
          </div>
          <button type="submit">Register</button>
        </form>
        <p className="login-link">
          Already have an account? <Link to="/">Login</Link>
        </p>
      </div>
      <div className="register-page-banner-container">
        {/* <img
          src={calorific_banner}
          alt="Calorific Banner"
          className="register-page-banner"
        /> */}
      </div>
    </div>
  );
};

export default Register;
