import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from './components/Navbar';
import ImageUpload from './components/ImageUpload';
import ResultsPanel from './components/ResultsPanel';
import axios from 'axios';

const SUPPORTED_ITEMS = [
  { value: "apple", label: "Apple" },
  { value: "banana", label: "Banana" },
  { value: "tomato", label: "Tomato" },
  { value: "orange", label: "Orange" },
  { value: "potato", label: "Potato" },
  { value: "cucumber", label: "Cucumber" },
  { value: "capsicum", label: "Capsicum" },
  { value: "okra", label: "Okra" }
];

function App() {
  const [selectedItem, setSelectedItem] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageSelect = useCallback((file) => {
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
      setError(null);
    }
  }, []);

  const handleAnalyze = async () => {
    if (!selectedImage || !selectedItem) {
      setError('Please select both an image and a fruit/vegetable type');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('fruit', selectedItem);

    try {
      const response = await axios.post('/api/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setResults(response.data);
      } else {
        setError(response.data.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setResults(null);
    setError(null);
    setSelectedItem('');
  };

  return (
    <div className="min-h-screen animated-gradient">
      <Navbar />
      
      <main className="container mx-auto px-4 py-6 lg:py-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Left Panel - Image Upload */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-6"
          >
            <ImageUpload
              selectedItem={selectedItem}
              setSelectedItem={setSelectedItem}
              items={SUPPORTED_ITEMS}
              onImageSelect={handleImageSelect}
              imagePreview={imagePreview}
              onAnalyze={handleAnalyze}
              onReset={handleReset}
              loading={loading}
              hasImage={!!selectedImage}
            />
            
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-2xl p-4 border border-red-500/30"
              >
                <div className="flex items-center gap-3 text-red-400">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-sm font-medium">{error}</span>
                </div>
              </motion.div>
            )}
          </motion.div>

          {/* Right Panel - Results */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <ResultsPanel results={results} loading={loading} />
          </motion.div>
        </div>

        {/* Footer Reference */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-10 text-center"
        >
          <div className="glass-light rounded-xl py-4 px-6 inline-block">
            <p className="text-dark-400 text-xs lg:text-sm">
              Prediction generated using CNN‑based visual analysis combined with
      produce‑specific non‑linear decay modeling.
            </p>
          </div>
        </motion.div>
      </main>
    </div>
  );
}

export default App;