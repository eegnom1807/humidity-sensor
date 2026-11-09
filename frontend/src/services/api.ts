import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost"
const API_PORT = import.meta.env.VITE_API_PORT || "3000"
const API_BASE_PATH = import.meta.env.VITE_API_BASE_PATH || "/api/v1"

export const API_ORIGIN = `${API_URL}:${API_PORT}`

export const api = axios.create({
  baseURL: `${API_ORIGIN}${API_BASE_PATH}`,
  headers: {
    "Content-Type": "application/json",
  },
})

export default api
