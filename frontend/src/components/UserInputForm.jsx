import { useState } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const UserInputForm = ({ setResumeData }) => {
  const [formData, setFormData] = useState({
    major: "Computer Science",
    industry: "Data Science",
    job_role: "Software Engineering",
    education: "Bachelor's degree in Computer Science",
    experience_years: "3",
    skills: ["Python", "Java", "JavaScript"],
    job_requirements: [
      "strong problem-solving skills",
      "experience in agile methodologies",
      "proficiency in Python and cloud services",
    ],
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSkillsChange = (e) => {
    const { value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      skills: value.split(",").map((skill) => skill.trim()),
    }));
  };

  const handleJobReqChange = (e) => {
    const { value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      job_requirements: value.split(",").map((req) => req.trim()),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/generate_resume",
        formData
      );
      console.log("Submitted data:", formData);
      console.log("API response:", response.data);
      setResumeData(response.data);
      navigate("/dashboard");
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  const LogoutUser = () => {
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <div className="user-input-form-container">
      <h2>User Input Form</h2>
      <button onClick={LogoutUser}>Logout</button>
      <form onSubmit={handleSubmit}>
        <label>
          Major:
          <input
            type="text"
            name="major"
            value={formData.major}
            onChange={handleChange}
          />
        </label>
        <label>
          Industry:
          <input
            type="text"
            name="industry"
            value={formData.industry}
            onChange={handleChange}
          />
        </label>
        <label>
          Job Role:
          <input
            type="text"
            name="job_role"
            value={formData.job_role}
            onChange={handleChange}
          />
        </label>
        <label>
          Education:
          <input
            type="text"
            name="education"
            value={formData.education}
            onChange={handleChange}
          />
        </label>
        <label>
          Experience (years):
          <input
            type="text"
            name="experience_years"
            value={formData.experience_years}
            onChange={handleChange}
          />
        </label>
        <label>
          Skills (comma-separated):
          <input
            type="text"
            name="skills"
            value={formData.skills.join(", ")}
            onChange={handleSkillsChange}
          />
        </label>
        <label>
          Job Requirements (comma-separated):
          <input
            type="text"
            name="job_requirements"
            value={formData.job_requirements.join(", ")}
            onChange={handleJobReqChange}
          />
        </label>
        <button type="submit">Generate Resume</button>
      </form>
    </div>
  );
};

UserInputForm.propTypes = {
  setResumeData: PropTypes.func.isRequired,
  resumeData: PropTypes.shape({
    success: PropTypes.bool,
    resume: PropTypes.object,
    resume_french: PropTypes.object,
  }),
};

export default UserInputForm;
