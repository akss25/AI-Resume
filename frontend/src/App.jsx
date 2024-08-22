import { useState } from "react";
import UserInputForm from "./components/UserInputForm";
import ResumeDisplay from "./components/ResumeDisplay";
import Login from "./components/Login";
import Register from "./components/Register";
import { Routes, Route } from "react-router-dom";

const App = () => {
  const [resumeData, setResumeData] = useState(null);

  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/build"
        element={
          <UserInputForm
            setResumeData={setResumeData}
            resumeData={resumeData}
          />
        }
      />
      <Route
        path="/dashboard"
        element={<ResumeDisplay resumeData={resumeData} />}
      />
    </Routes>
  );
};

export default App;
