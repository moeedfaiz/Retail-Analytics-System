import { useState } from "react";

import Navbar from "./components/Navbar";
import UploadCard from "./components/UploadCard";
import ResultImage from "./components/ResultImage";
import Analytics from "./components/Analytics";

import "./App.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app">
      <Navbar />

      <main className="main-container">
        <UploadCard setResult={setResult} />

        {result && (
          <>
            <ResultImage result={result} />
            <Analytics result={result} />
          </>
        )}
      </main>
    </div>
  );
}

export default App;