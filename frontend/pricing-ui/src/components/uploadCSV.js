import React, { useState } from "react";
import API from "../api";

const UploadCSV = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file to upload.");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await API.post("/upload/", formData);
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Upload failed: " + error.response.data.error);
    }
  };

  return (
    <div>
      <h2>Upload CSV File</h2>
      <input type="file" onChange={handleFileChange} accept=".csv" />
      <button onClick={handleUpload}>Upload</button>
      <p>{message}</p>
    </div>
  );
};

export default UploadCSV;
