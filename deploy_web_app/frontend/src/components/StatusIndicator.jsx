import React from 'react';
import { motion } from 'framer-motion';

const StatusIndicator = ({ status, color }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'FRESH':
        return {
          bg: 'from-green-500/20 to-green-600/10',
          border: 'border-green-500/50',
          glow: 'glow-green',
          icon: '✓',
          message: 'This produce is fresh and safe to consume!',
          tips: ['Store properly to maintain freshness', 'Consume within recommended time']
        };
      case 'CONSUME SOON':
        return {
          bg: 'from-amber-500/20 to-amber-600/10',
          border: 'border-amber-500/50',
          glow: 'glow-amber',
          icon: '⚠',
          message: 'This produce should be consumed soon.',
          tips: ['Use within 1-2 days', 'Check for any soft spots before consuming']
        };
      case 'SPOILED':
        return {
          bg: 'from-red-500/20 to-red-600/10',
          border: 'border-red-500/50',
          glow: 'glow-red',
          icon: '✕',
          message: 'This produce appears to be spoiled.',
          tips: ['Do not consume', 'Dispose of properly', 'Check other stored items']
        };
      default:
        return {
          bg: 'from-gray-500/20 to-gray-600/10',
          border: 'border-gray-500/50',
          glow: '',
          icon: '?',
          message: 'Status unknown',
          tips: []
        };
    }
  };

  const config = getStatusConfig();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`glass rounded-3xl p-6 lg:p-8 bg-gradient-to-br ${config.bg} ${config.border} border ${config.glow}`}
    >
      <div className="flex items-center gap-4 mb-4">
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="w-14 h-14 lg:w-16 lg:h-16 rounded-full flex items-center justify-center text-2xl lg:text-3xl"
          style={{ backgroundColor: `${color}20`, border: `2px solid ${color}` }}
        >
          <span style={{ color }}>{config.icon}</span>
        </motion.div>
        <div>
          <p className="text-dark-400 text-sm mb-1">Final Status</p>
          <h3 
            className="text-2xl lg:text-3xl font-bold"
            style={{ color }}
          >
            {status}
          </h3>
        </div>
      </div>

      <p className="text-dark-300 mb-4">{config.message}</p>

      {config.tips.length > 0 && (
        <div className="space-y-2">
          <p className="text-dark-400 text-sm font-medium">Recommendations:</p>
          <ul className="space-y-1">
            {config.tips.map((tip, index) => (
              <li key={index} className="flex items-center gap-2 text-dark-300 text-sm">
                <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: color }} />
                {tip}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
};

export default StatusIndicator;