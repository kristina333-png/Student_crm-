import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:5173/api",
  headers: {
    "Content-Type": "application/json",
    "X-User-Role": "admin",
  },
});

export default apiClient;