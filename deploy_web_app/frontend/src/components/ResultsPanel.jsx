import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import StatusIndicator from './StatusIndicator';
import FreshnessChart from './FreshnessChart';

const ResultsPanel = ({ results, loading }) => {
  if (loading) {
    return (
      <div className="glass rounded-3xl p-6 lg:p-8 min-h-[500px] flex items-center justify-center">
        <div className="text-center">
          <div className="loader w-12 h-12 mx-auto mb-4"></div>
          <p className="text-dark-300">Analyzing your produce...</p>
          <p className="text-dark-500 text-sm mt-1">This may take a few seconds</p>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="glass rounded-3xl p-6 lg:p-8 min-h-[500px] flex items-center justify-center">
        <div className="text-center">
          <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-dark-700/50 flex items-center justify-center">
            <svg className="w-10 h-10 text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-dark-300 mb-2">No Results Yet</h3>
          <p className="text-dark-500 text-sm max-w-xs mx-auto">
            Upload an image and select a produce type to see freshness analysis results
          </p>
        </div>
      </div>
    );
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="space-y-6"
      >
        {/* Results Header */}
        <div className="glass rounded-3xl p-6 lg:p-8">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-primary-500/20 flex items-center justify-center">
              <svg className="w-5 h-5 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <h2 className="text-lg lg:text-xl font-semibold text-white">Analysis Results</h2>
              <p className="text-dark-400 text-sm">{results.fruit} Freshness Report</p>
            </div>
          </div>

          {/* Freshness Metrics Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
            <MetricCard
              title="Ideal Storage"
              value={`${results.decay.ideal_final}%`}
              subtitle={`${results.decay.ideal_days_left} days left`}
              icon="❄️"
              color="blue"
            />
            <MetricCard
              title="Room Temperature"
              value={`${results.decay.room_final}%`}
              subtitle={`${results.decay.room_days_left} days left`}
              icon="🏠"
              color="amber"
            />
            <MetricCard
              title="High Humidity"
              value={`${results.decay.humid_final}%`}
              subtitle={`${results.decay.humid_days_left} days left`}
              icon="💧"
              color="red"
            />
          </div>

          {/* Initial Freshness */}
          <div className="glass-light rounded-xl p-4 mb-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-dark-400 text-sm">Initial Freshness Score</p>
                <p className="text-2xl font-bold text-white">{results.initial_freshness}%</p>
              </div>
              <div className="w-16 h-16 rounded-full border-4 border-primary-500 flex items-center justify-center">
                <span className="text-lg font-bold text-primary-400">{Math.round(results.initial_freshness)}</span>
              </div>
            </div>
            <div className="mt-3 h-2 bg-dark-700 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${results.initial_freshness}%` }}
                transition={{ duration: 1, ease: "easeOut" }}
                className="h-full bg-gradient-to-r from-primary-600 to-primary-400 rounded-full"
              />
            </div>
          </div>

          {/* Shelf Life Info */}
          <div className="grid grid-cols-3 gap-3">
            <div className="text-center p-3 rounded-xl bg-dark-700/30">
              <p className="text-xs text-dark-400">Ideal Shelf</p>
              <p className="text-lg font-semibold text-white">{results.shelf_life.ideal}d</p>
            </div>
            <div className="text-center p-3 rounded-xl bg-dark-700/30">
              <p className="text-xs text-dark-400">Room Shelf</p>
              <p className="text-lg font-semibold text-white">{results.shelf_life.room}d</p>
            </div>
            <div className="text-center p-3 rounded-xl bg-dark-700/30">
              <p className="text-xs text-dark-400">Humid Shelf</p>
              <p className="text-lg font-semibold text-white">{results.shelf_life.humid}d</p>
            </div>
          </div>
        </div>

        {/* Status Indicator */}
        <StatusIndicator status={results.status} color={results.status_color} />

        {/* Chart */}
        <FreshnessChart data={results.chart_data} />
      </motion.div>
    </AnimatePresence>
  );
};

const MetricCard = ({ title, value, subtitle, icon, color }) => {
  const colorClasses = {
    blue: 'from-blue-500/20 to-blue-600/10 border-blue-500/30',
    amber: 'from-amber-500/20 to-amber-600/10 border-amber-500/30',
    red: 'from-red-500/20 to-red-600/10 border-red-500/30',
    green: 'from-green-500/20 to-green-600/10 border-green-500/30',
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className={`p-4 rounded-xl bg-gradient-to-br ${colorClasses[color]} border transition-all duration-200`}
    >
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xl">{icon}</span>
        <span className="text-dark-300 text-xs font-medium">{title}</span>
      </div>
      <p className="text-1xl font-bold text-white">{subtitle}</p>
      <p className="text-dark-400 text-xs mt-1">{value}</p>
    </motion.div>
  );
};

export default ResultsPanel;