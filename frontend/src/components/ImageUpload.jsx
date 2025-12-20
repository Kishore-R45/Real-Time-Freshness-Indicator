import React, { useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const ImageUpload = ({
  selectedItem,
  setSelectedItem,
  items,
  onImageSelect,
  imagePreview,
  onAnalyze,
  onReset,
  loading,
  hasImage
}) => {
  const fileInputRef = useRef(null);
  const cameraInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onImageSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onImageSelect(e.target.files[0]);
    }
  };

  return (
    <div className="glass rounded-3xl p-6 lg:p-8 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-primary-500/20 flex items-center justify-center">
          <svg className="w-5 h-5 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <h2 className="text-lg lg:text-xl font-semibold text-white">Upload & Analyze</h2>
          {/* <p className="text-dark-400 text-sm hidden sm:block">Select your produce for analysis</p> */}
        </div>
      </div>

      {/* Dropdown */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-dark-300">
          Select Fruit or Vegetable
        </label>
        <select
          value={selectedItem}
          onChange={(e) => setSelectedItem(e.target.value)}
          className="w-full px-4 py-3 lg:py-4 rounded-xl bg-dark-800/50 border border-dark-600 text-white focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all duration-200 cursor-pointer text-sm lg:text-base"
        >
          <option value="">Choose an item...</option>
          {items.map((item) => (
            <option key={item.value} value={item.value}>
              {item.label}
            </option>
          ))}
        </select>
      </div>

      {/* Upload Area */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`relative rounded-2xl border-2 border-dashed transition-all duration-300 ${
          dragActive 
            ? 'border-primary-400 bg-primary-500/10' 
            : 'border-dark-600 hover:border-dark-500'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="hidden"
        />
        <input
          ref={cameraInputRef}
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleFileChange}
          className="hidden"
        />

        <AnimatePresence mode="wait">
          {imagePreview ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="p-4"
            >
              <div className="relative rounded-xl overflow-hidden">
                <img
                  src={imagePreview}
                  alt="Selected"
                  className="w-full h-48 lg:h-64 object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-dark-900/60 to-transparent" />
                <button
                  onClick={onReset}
                  className="absolute top-3 right-3 w-8 h-8 rounded-full bg-dark-900/80 hover:bg-red-500 transition-colors flex items-center justify-center"
                >
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="p-8 lg:p-12 text-center"
            >
              <div className="w-16 h-16 lg:w-20 lg:h-20 mx-auto mb-4 rounded-full bg-dark-700/50 flex items-center justify-center">
                <svg className="w-8 h-8 lg:w-10 lg:h-10 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <p className="text-dark-300 mb-1 text-sm lg:text-base">
                Drag & drop your image here
              </p>
              <p className="text-dark-500 text-xs lg:text-sm">
                or use the buttons below
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Action Buttons - FIXED */}
      
      {/* Mobile: 2 buttons (Upload + Camera) */}
      <div className="grid grid-cols-2 gap-3 lg:hidden">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => fileInputRef.current?.click()}
          className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-dark-700/50 hover:bg-dark-700 border border-dark-600 text-white transition-all duration-200"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          <span className="text-sm font-medium">Upload</span>
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => cameraInputRef.current?.click()}
          className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-dark-700/50 hover:bg-dark-700 border border-dark-600 text-white transition-all duration-200"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span className="text-sm font-medium">Camera</span>
        </motion.button>
      </div>

      {/* Desktop: 1 button (Full width) */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={() => fileInputRef.current?.click()}
        className="hidden lg:flex w-full items-center justify-center gap-2 px-4 py-3 rounded-xl bg-dark-700/50 hover:bg-dark-700 border border-dark-600 text-white transition-all duration-200"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
        <span className="text-sm font-medium">Browse & Upload Image</span>
      </motion.button>

      {/* Analyze Button */}
      <motion.button
        whileHover={{ scale: hasImage && selectedItem ? 1.02 : 1 }}
        whileTap={{ scale: hasImage && selectedItem ? 0.98 : 1 }}
        onClick={onAnalyze}
        disabled={!hasImage || !selectedItem || loading}
        className={`w-full py-4 rounded-xl font-semibold text-white transition-all duration-300 flex items-center justify-center gap-3 ${
          hasImage && selectedItem && !loading
            ? 'bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400 glow-green cursor-pointer'
            : 'bg-dark-700 cursor-not-allowed opacity-50'
        }`}
      >
        {loading ? (
          <>
            <div className="loader w-5 h-5"></div>
            <span>Analyzing...</span>
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            <span>Analyze Freshness</span>
          </>
        )}
      </motion.button>
    </div>
  );
};

export default ImageUpload;