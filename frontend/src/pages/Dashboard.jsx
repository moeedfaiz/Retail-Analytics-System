import { useState } from 'react';

import Navbar from '../components/Navbar';
import UploadCard from '../components/UploadCard';
import Analytics from '../components/Analytics';
import ResultImage from '../components/ResultImage';

export default function Dashboard() {
  const [result, setResult] = useState(null);

  return (
    <div>
      <Navbar />

      <UploadCard setResult={setResult} />

      {result && (
        <>
          <ResultImage image={result.output_image} />

          <Analytics data={result} />
        </>
      )}
    </div>
  );
}
