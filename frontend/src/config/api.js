const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export const API_ENDPOINTS = {
  health: `${API_BASE_URL}/api/health`,
  items: `${API_BASE_URL}/api/items`,
  predict: `${API_BASE_URL}/api/predict`,
};

export default API_BASE_URL;