import api from "./api"
import type { Sensor, SensorRequest, SensorResponse, SensorsResponse } from "@/types/sensor"

export const sensorService = {
  getAll: async (): Promise<Sensor[]> => {
    const response = await api.get<SensorsResponse>("/sensors")
    return response.data.data
  },

  create: async (data: SensorRequest): Promise<Sensor> => {
    const response = await api.post<SensorResponse>("/sensors", data)
    return response.data.data
  },

  update: async (id: number, data: SensorRequest): Promise<Sensor> => {
    const response = await api.put<SensorResponse>(`/sensors/${id}`, data)
    return response.data.data
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/sensors/${id}`)
  },
}

export default sensorService
