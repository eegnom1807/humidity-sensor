import { api } from "./api"
import type { ApiResponse } from "@/types/api"
import type { Sensor, SensorRequest } from "@/types/sensor"

export const sensorService = {
  getAll: async (): Promise<Sensor[]> => {
    const response = await api.get<ApiResponse<Sensor[]>>("/sensors")
    return response.data.data
  },

  create: async (data: SensorRequest): Promise<Sensor> => {
    const response = await api.post<ApiResponse<Sensor>>("/sensors", data)
    return response.data.data
  },

  update: async (id: number, data: SensorRequest): Promise<Sensor> => {
    const response = await api.put<ApiResponse<Sensor>>(`/sensors/${id}`, data)
    return response.data.data
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/sensors/${id}`)
  },
}
