import { useState } from "react";
import FileUploader from "./components/FileUploader";
import ResultViewer from "./components/ResultViewer";
import LoadingSpinner from "./components/LoadingSpinner";
import { uploadFile, processDocument } from "./services/api";
import "./index.css";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

const handleUpload = async (file) => {
  try {
    setLoading(true);
    setError("");
    setResult(null);

    console.log("Uploading file:", file.name);

    // Step 1: Upload document
    const uploadRes = await uploadFile(file);

    console.log("Upload Response:", uploadRes);
    console.log("Upload Data:", uploadRes.data);

    // Backend returns path inside response.data
    const filePath = uploadRes.data?.path;

    if (!filePath) {
      throw new Error("Backend did not return a file path.");
    }

    console.log("File uploaded successfully.");
    console.log("Path:", filePath);

    // Step 2: Process document
    console.log("Calling /process...");

    const processRes = await processDocument(filePath);

    console.log("Process Response:", processRes);
    console.log("Process Data:", processRes.data);

    // Axios response -> actual backend JSON
    setResult(processRes.data);

  } catch (err) {
    console.error("ERROR:", err);

    if (err.response) {
      console.error("Status:", err.response.status);
      console.error("Backend response:", err.response.data);

      setError(
        err.response.data?.detail ||
        err.response.data?.message ||
        `Server error: ${err.response.status}`
      );
    } else {
      setError(err.message || "Failed to process document.");
    }
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="app">

      {/* Background decorations */}
      <div className="bg-circle circle-one"></div>
      <div className="bg-circle circle-two"></div>

      {/* Navbar */}
      <nav className="navbar">
        <div className="brand">
          <div className="brand-icon">✦</div>

          <div>
            <h2>TeacherAI</h2>
            <span>Knowledge Studio</span>
          </div>
        </div>

        <div className="nav-badge">
          <span className="status-dot"></span>
          Local AI
        </div>
      </nav>

      {/* Hero */}
      <main className="main-container">

        <section className="hero">

          <div className="hero-badge">
            ✨ AI-Powered Education
          </div>

          <h1>
            Turn documents into
            <span> smarter lessons.</span>
          </h1>

          <p>
            Upload your educational material and let AI transform it
            into a structured Teacher Knowledge Package with objectives,
            concepts, activities and assessments.
          </p>

        </section>

        {/* Upload card */}
        <section className="upload-section">

          <div className="section-heading">
            <div>
              <span className="eyebrow">STEP 01</span>
              <h2>Upload your document</h2>
              <p>
                Start with a PDF, Word document, text file or Markdown file.
              </p>
            </div>
          </div>

          <FileUploader onUpload={handleUpload} />

        </section>

        {/* Processing */}
        {loading && (
          <section className="processing-card">

            <div className="processing-icon">
              ✨
            </div>

            <div>
              <h3>Creating your Knowledge Package</h3>

              <p>
                Reading document, extracting concepts and generating
                teacher-ready content...
              </p>

              <div className="progress-track">
                <div className="progress-bar"></div>
              </div>
            </div>

          </section>
        )}

        {/* Error */}
        {error && (
          <section className="error-card">

            <div className="error-icon">
              !
            </div>

            <div>
              <h3>Something went wrong</h3>
              <p>{error}</p>
            </div>

          </section>
        )}

        {/* Result */}
        {result && !loading && (
          <section className="result-section">

            <div className="section-heading">

              <div>
                <span className="eyebrow">STEP 02</span>

                <h2>Your Teacher Knowledge Package</h2>

                <p>
                  AI-generated teaching material based on your document.
                </p>
              </div>

              <div className="success-badge">
                ✓ Generated
              </div>

            </div>

            <ResultViewer result={result} />

          </section>
        )}

        {/* Empty state */}
        {!result && !loading && !error && (
          <section className="features">

            <div className="feature-card">
              <div className="feature-icon purple">
                🧠
              </div>

              <h3>Smart Extraction</h3>

              <p>
                Automatically identify important concepts and information.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon blue">
                🎯
              </div>

              <h3>Learning Objectives</h3>

              <p>
                Generate clear and measurable objectives for teachers.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon orange">
                📝
              </div>

              <h3>Assessments</h3>

              <p>
                Create activities and assessments from your content.
              </p>
            </div>

          </section>
        )}

      </main>

      <footer>
        <span>TeacherAI Knowledge Studio</span>
      </footer>

    </div>
  );
}
