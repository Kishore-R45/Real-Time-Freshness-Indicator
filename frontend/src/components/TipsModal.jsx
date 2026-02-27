import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const CONDITION_CONFIG = {
  ideal: {
    label: 'Ideal Storage',
    icon: '❄️',
    color: 'blue',
    gradient: 'from-blue-500/20 to-blue-600/10',
    border: 'border-blue-500/40',
    textColor: 'text-blue-400',
    dotColor: 'bg-blue-400',
  },
  room: {
    label: 'Room Temperature',
    icon: '🏠',
    color: 'amber',
    gradient: 'from-amber-500/20 to-amber-600/10',
    border: 'border-amber-500/40',
    textColor: 'text-amber-400',
    dotColor: 'bg-amber-400',
  },
  high_humidity: {
    label: 'High Humidity',
    icon: '💧',
    color: 'red',
    gradient: 'from-red-500/20 to-red-600/10',
    border: 'border-red-500/40',
    textColor: 'text-red-400',
    dotColor: 'bg-red-400',
  },
};

const TipsModal = ({ tips, fruit, onClose }) => {
  const [activeTab, setActiveTab] = useState('ideal');

  if (!tips) return null;

  const conditions = Object.keys(CONDITION_CONFIG);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        {/* Backdrop */}
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />

        {/* Modal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 20 }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          onClick={(e) => e.stopPropagation()}
          className="relative w-full max-w-lg max-h-[85vh] overflow-hidden glass rounded-3xl border border-dark-600/50 shadow-2xl"
        >
          {/* Header */}
          <div className="p-6 pb-4 border-b border-dark-700/50">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-primary-500/20 flex items-center justify-center">
                  <span className="text-xl">💡</span>
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-white">Storage Tips</h2>
                  <p className="text-dark-400 text-sm">How to store {fruit} properly</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="w-8 h-8 rounded-lg bg-dark-700/50 hover:bg-dark-600/50 flex items-center justify-center text-dark-400 hover:text-white transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 mt-4">
              {conditions.map((key) => {
                const cfg = CONDITION_CONFIG[key];
                const isActive = activeTab === key;
                return (
                  <button
                    key={key}
                    onClick={() => setActiveTab(key)}
                    className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium transition-all duration-200 ${
                      isActive
                        ? `bg-gradient-to-br ${cfg.gradient} ${cfg.border} border ${cfg.textColor}`
                        : 'bg-dark-700/30 text-dark-400 hover:text-dark-300 border border-transparent'
                    }`}
                  >
                    <span>{cfg.icon}</span>
                    <span>{cfg.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Tips Content */}
          <div className="p-6 overflow-y-auto max-h-[50vh]">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                transition={{ duration: 0.2 }}
                className="space-y-3"
              >
                {tips[activeTab]?.map((tip, index) => {
                  const cfg = CONDITION_CONFIG[activeTab];
                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.06 }}
                      className="flex items-start gap-3 p-3 rounded-xl bg-dark-700/20 hover:bg-dark-700/40 transition-colors"
                    >
                      <span className={`w-2 h-2 rounded-full ${cfg.dotColor} mt-1.5 flex-shrink-0`} />
                      <p className="text-dark-300 text-sm leading-relaxed">{tip}</p>
                    </motion.div>
                  );
                })}
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-dark-700/50">
            <p className="text-dark-500 text-xs text-center">
              Tips are tailored for {fruit}. Always inspect produce before consuming.
            </p>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default TipsModal;
