import { useState } from "react";
import { FaCloudUploadAlt, FaImage, FaSpinner } from "react-icons/fa";
import api from "../services/api";

export default function UploadCard({ setResult }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileSelect = (selectedFile) => {
    if (!selectedFile) return;

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setResult(null);
  };

  const upload = async () => {
    if (!file) {
      alert("Please select an image first.");
      return;
    }

    const form = new FormData();
    form.append("image", file);

    setLoading(true);

    try {
      const res = await api.post("/analyze", form, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (!res.data.success) {
        alert(res.data.message || "Analysis failed.");
        setLoading(false);
        return;
      }

      res.data.originalImage = preview;
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Unable to connect to backend. Make sure Flask is running on port 5000.");
    }

    setLoading(false);
  };

  return (
    <section className="upload-card">
      <div className="section-title">
        <h2>Upload Chiller Image</h2>
        <p>Select a retail chiller image and run AI analytics.</p>
      </div>

      <label className="upload-box">
        <FaCloudUploadAlt className="upload-icon" />
        <h3>Choose Image</h3>
        <p>Supports JPG, PNG, JPEG, WEBP</p>

        <input
          type="file"
          accept="image/*"
          hidden
          onChange={(e) => handleFileSelect(e.target.files[0])}
        />
      </label>

      {preview && (
        <div className="preview-box">
          <img src={preview} alt="Selected Preview" />
        </div>
      )}

      <button
        className="analyze-btn"
        onClick={upload}
        disabled={loading}
      >
        {loading ? (
          <>
            <FaSpinner className="spinner" />
            Processing Image...
          </>
        ) : (
          <>
            <FaImage />
            Analyze Image
          </>
        )}
      </button>
    </section>
  );
}