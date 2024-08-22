import { useEffect, useState } from "react";
import { IoIosArrowRoundBack } from "react-icons/io";
import PropTypes from "prop-types";
import html2pdf from "html2pdf.js";
import { useNavigate } from "react-router-dom";

const ResumeDisplay = ({ resumeData }) => {
  const [downloadLinks, setDownloadLinks] = useState({
    resume: null,
    resume_french: null,
  });

  useEffect(() => {
    if (resumeData?.success) {
      const pdfOptions = {
        margin: 10,
        filename: "resume.pdf",
        image: { type: "jpeg", quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
      };

      // Generate PDF for the English resume
      if (resumeData.resume) {
        html2pdf()
          .from(document.getElementById("englishResumeContent"))
          .set(pdfOptions)
          .outputPdf("blob")
          .then((pdf) => {
            const url = URL.createObjectURL(pdf);
            setDownloadLinks((prevLinks) => ({ ...prevLinks, resume: url }));
          });
      }

      // Generate PDF for the French resume
      if (resumeData.resume_french) {
        html2pdf()
          .from(document.getElementById("frenchResumeContent"))
          .set(pdfOptions)
          .outputPdf("blob")
          .then((pdf) => {
            const url = URL.createObjectURL(pdf);
            setDownloadLinks((prevLinks) => ({
              ...prevLinks,
              resume_french: url,
            }));
          });
      }
    }
  }, [resumeData]);

  const navigate = useNavigate();
  const GoBackToResumeBuilder = () => {
    navigate("/build");
  };

  return (
    <div>
      <h2>Resume Display</h2>
      <IoIosArrowRoundBack onClick={GoBackToResumeBuilder} />
      <div>
        {/* Display the English resume content */}
        {resumeData?.resume && (
          <div id="englishResumeContent">
            <h3>English Resume:</h3>
            {resumeData.resume.Name && (
              <>
                <h4>Name:</h4>
                <p>{resumeData.resume.Name}</p>
              </>
            )}
            {resumeData.resume.Objective && (
              <>
                <h4>Objective:</h4>
                <p>{resumeData.resume.Objective}</p>
              </>
            )}
            {resumeData.resume.Skills &&
              resumeData.resume.Skills.length > 0 && (
                <>
                  <h4>Skills:</h4>
                  <ul>
                    {resumeData.resume.Skills.map((skill, index) => (
                      <li key={index}>{skill}</li>
                    ))}
                  </ul>
                </>
              )}
            {resumeData.resume["Work Experience"] && (
              <>
                <h4>Work Experience:</h4>
                {resumeData.resume["Work Experience"].Title && (
                  <p>
                    <strong>Title:</strong>{" "}
                    {resumeData.resume["Work Experience"].Title}
                  </p>
                )}
                {resumeData.resume["Work Experience"].Duration && (
                  <p>
                    <strong>Duration:</strong>{" "}
                    {resumeData.resume["Work Experience"].Duration}
                  </p>
                )}
                {resumeData.resume["Work Experience"].Description && (
                  <p>
                    <strong>Description:</strong>{" "}
                    {resumeData.resume["Work Experience"].Description}
                  </p>
                )}
              </>
            )}
            {resumeData.resume["Additional Qualifications"] &&
              resumeData.resume["Additional Qualifications"].length > 0 && (
                <>
                  <h4>Additional Qualifications:</h4>
                  <ul>
                    {resumeData.resume["Additional Qualifications"].map(
                      (qualification, index) => (
                        <li key={index}>{qualification}</li>
                      )
                    )}
                  </ul>
                </>
              )}
          </div>
        )}
        {/* Display the French resume content */}
        {resumeData?.resume_french && (
          <div id="frenchResumeContent">
            <h3>French Resume:</h3>
            {resumeData.resume_french.Nom && (
              <>
                <h4>Nom:</h4>
                <p>{resumeData.resume_french.Nom}</p>
              </>
            )}
            {resumeData.resume_french.Objectif && (
              <>
                <h4>Objectif:</h4>
                <p>{resumeData.resume_french.Objectif}</p>
              </>
            )}
            {resumeData.resume_french.Compétences &&
              resumeData.resume_french.Compétences.length > 0 && (
                <>
                  <h4>Compétences:</h4>
                  <ul>
                    {resumeData.resume_french.Compétences.map(
                      (competence, index) => (
                        <li key={index}>{competence}</li>
                      )
                    )}
                  </ul>
                </>
              )}
            {resumeData.resume_french["Expérience Professionnelle"] && (
              <>
                <h4>Expérience Professionnelle:</h4>
                {resumeData.resume_french["Expérience Professionnelle"]
                  .Titre && (
                  <p>
                    <strong>Titre:</strong>{" "}
                    {
                      resumeData.resume_french["Expérience Professionnelle"]
                        .Titre
                    }
                  </p>
                )}
                {resumeData.resume_french["Expérience Professionnelle"]
                  .Durée && (
                  <p>
                    <strong>Durée:</strong>{" "}
                    {
                      resumeData.resume_french["Expérience Professionnelle"]
                        .Durée
                    }
                  </p>
                )}
                {resumeData.resume_french["Expérience Professionnelle"]
                  .Description && (
                  <p>
                    <strong>Description:</strong>{" "}
                    {
                      resumeData.resume_french["Expérience Professionnelle"]
                        .Description
                    }
                  </p>
                )}
              </>
            )}
            {resumeData.resume_french["Qualifications Supplémentaires"] &&
              resumeData.resume_french["Qualifications Supplémentaires"]
                .length > 0 && (
                <>
                  <h4>Qualifications supplémentaires:</h4>
                  <ul>
                    {resumeData.resume_french[
                      "Qualifications Supplémentaires"
                    ].map((qualification, index) => (
                      <li key={index}>{qualification}</li>
                    ))}
                  </ul>
                </>
              )}
            {resumeData.resume_french.Éducation && (
              <>
                <h4>Éducation:</h4>
                {resumeData.resume_french.Éducation.Diplôme && (
                  <p>
                    <strong>Diplôme:</strong>{" "}
                    {resumeData.resume_french.Éducation.Diplôme}
                  </p>
                )}
                {resumeData.resume_french.Éducation.Université && (
                  <p>
                    <strong>Université:</strong>{" "}
                    {resumeData.resume_french.Éducation.Université}
                  </p>
                )}
                {resumeData.resume_french.Éducation.Année && (
                  <p>
                    <strong>Année:</strong>{" "}
                    {resumeData.resume_french.Éducation.Année}
                  </p>
                )}
              </>
            )}
          </div>
        )}
      </div>

      {/* Download links */}
      <div>
        <p>Download Links:</p>
        {downloadLinks.resume && (
          <a
            href={downloadLinks.resume}
            target="_blank"
            rel="noopener noreferrer"
            download="English_Resume.pdf"
          >
            Download English Resume PDF
          </a>
        )}
        {downloadLinks.resume_french && (
          <a
            href={downloadLinks.resume_french}
            target="_blank"
            rel="noopener noreferrer"
            download="French_Resume.pdf"
          >
            Download French Resume PDF
          </a>
        )}
      </div>
    </div>
  );
};

ResumeDisplay.propTypes = {
  resumeData: PropTypes.shape({
    success: PropTypes.bool,
    resume: PropTypes.shape({
      Name: PropTypes.string,
      Objective: PropTypes.string,
      Skills: PropTypes.arrayOf(PropTypes.string),
      "Work Experience": PropTypes.shape({
        Title: PropTypes.string,
        Duration: PropTypes.string,
        Description: PropTypes.string,
      }),
      "Additional Qualifications": PropTypes.arrayOf(PropTypes.string),
    }),
    resume_french: PropTypes.shape({
      Nom: PropTypes.string,
      Objectif: PropTypes.string,
      Compétences: PropTypes.arrayOf(PropTypes.string),
      "Expérience Professionnelle": PropTypes.shape({
        Titre: PropTypes.string,
        Durée: PropTypes.string,
        Description: PropTypes.string,
      }),
      "Qualifications Supplémentaires": PropTypes.arrayOf(PropTypes.string),
      Éducation: PropTypes.shape({
        Diplôme: PropTypes.string,
        Université: PropTypes.string,
        Année: PropTypes.string,
      }),
    }),
  }),
};

export default ResumeDisplay;
