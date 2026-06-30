export default function ResultImage({ result }) {
  if (!result) return null;

  return (
    <section className="result-section">
      <div className="section-title">
        <h2>Detection Results</h2>
        <p>Original image compared with AI-processed output.</p>
      </div>

      <div className="image-grid">
        <div className="image-card">
          <h3>Original Image</h3>

          {result.originalImage ? (
            <img src={result.originalImage} alt="Original" />
          ) : (
            <div className="empty-image">No original preview</div>
          )}
        </div>

        <div className="image-card">
          <h3>Processed Image</h3>

          <img src={result.output_image} alt="Processed Result" />
        </div>
      </div>
    </section>
  );
}