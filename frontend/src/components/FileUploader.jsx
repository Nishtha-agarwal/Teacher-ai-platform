import { useState } from "react";

export default function FileUploader({ onUpload }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleSubmit = () => {
    if (!selectedFile) {
      alert("Please select a file");
      return;
    }

    onUpload(selectedFile);
  };

  return (
    <div>
      <h2>Upload Document</h2>

      <input
        type="file"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />

      <button onClick={handleSubmit}>
        Upload
      </button>
    </div>
  );
}