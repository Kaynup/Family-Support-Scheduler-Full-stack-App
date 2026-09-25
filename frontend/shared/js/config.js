// Centralized API configuration — imported by all panels.
const isLocal = typeof window !== "undefined" && 
  (window.location.hostname === "localhost" || 
   window.location.hostname === "127.0.0.1" || 
   window.location.hostname === "");

export const API_BASE_URL = (typeof window !== "undefined" && window.__API_BASE_URL__)
  ? window.__API_BASE_URL__
  : isLocal
    ? "http://127.0.0.1:8000"
    : "https://family-scheduler-api.onrender.com";
