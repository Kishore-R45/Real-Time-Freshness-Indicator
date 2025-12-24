import React from 'react';
import { motion } from 'framer-motion';

const Navbar = () => {
  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="glass sticky top-0 z-50"
    >
      <div className="container mx-auto px-4 py-4 lg:py-5">
        <div className="flex items-center justify-center">
          <div className="flex items-center gap-3">
            {/* Logo Icon */}
            <motion.div
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.5 }}
              className="w-10 h-10 lg:w-12 lg:h-12 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg glow-green"
            >
              <svg 
                className="w-6 h-6 lg:w-7 lg:h-7 text-white" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" 
                />
              </svg>
            </motion.div>
            
            {/* Title */}
            <div className="text-center lg:text-left">
              <h1 className="text-xl lg:text-2xl xl:text-3xl font-bold gradient-text tracking-tight">
                Real-Time Freshness Indicator
              </h1>
              {/* <p className="text-dark-400 text-xs lg:text-sm hidden sm:block">
                AI-Powered Quality Assessment
              </p> */}
            </div>
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;