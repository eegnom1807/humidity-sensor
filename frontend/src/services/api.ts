import axios from "axios"

export const API_ORIGIN = import.meta.env.VITE_API_URL || "http://localhost:3000"

export const api = axios.create({
  baseURL: `${API_ORIGIN}/api/v1`,
})

export default api
