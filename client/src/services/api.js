import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor — attach JWT token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('chandas_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor — handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('chandas_token');
      // Optionally redirect to login
    }
    return Promise.reject(error);
  }
);

// === API Functions ===

// Health
export const checkHealth = () => api.get('/health');

// Chandas Analysis
export const analyzeVerse = (text, script = 'devanagari', enableSandhi = false) =>
  api.post('/chandas/analyze', { text, script, enable_sandhi: enableSandhi });

export const listMeters = (params = {}) =>
  api.get('/chandas/meters', { params });

export const getMeter = (meterId) =>
  api.get(`/chandas/meters/${meterId}`);

export const syllabify = (text, script = 'devanagari') =>
  api.post('/chandas/syllabify', { text, script });

// Translation
export const translate = (text, targetLanguage = 'hindi') =>
  api.post('/translate', { text, target_language: targetLanguage });

export const translatePadaccheda = (text, targetLanguage = 'hindi') =>
  api.post('/translate/padaccheda', { text, target_language: targetLanguage });

export const getLanguages = () =>
  api.get('/translate/languages');

// OCR
export const extractText = (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  return api.post('/ocr/extract', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

// Auth
export const register = (username, email, password) =>
  api.post('/auth/register', { username, email, password });

export const login = (email, password) =>
  api.post('/auth/login', { email, password });

export const getProfile = () =>
  api.get('/auth/profile');

// History
export const getHistory = (params = {}) =>
  api.get('/history', { params });

export const getHistoryItem = (id) =>
  api.get(`/history/${id}`);

export const deleteHistoryItem = (id) =>
  api.delete(`/history/${id}`);

export default api;
