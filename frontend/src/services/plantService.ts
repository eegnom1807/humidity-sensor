import { api, API_ORIGIN } from "./api"
import type { ApiResponse } from "@/types/api"
import type { Plant, PlantRequest, DashboardPlant } from "@/types/plant"

export const plantService = {
  // Get dashboard data
  getDashboard: async (): Promise<DashboardPlant[]> => {
    const response = await api.get<ApiResponse<DashboardPlant[]>>("/plants/dashboard");
    return response.data.data;
  },

  // Get all plants
  getAll: async (): Promise<Plant[]> => {
    const response = await api.get<ApiResponse<Plant[]>>("/plants");
    return response.data.data;
  },

  // Create plant
  create: async (data: PlantRequest): Promise<Plant> => {
    const response = await api.post<ApiResponse<Plant>>("/plants", data)
    return response.data.data
  },

  // Update plant
  update: async (id: number, data: PlantRequest): Promise<Plant> => {
    const response = await api.put<ApiResponse<Plant>>(`/plants/${id}`, data)
    return response.data.data
  },

  // Delete plant
  delete: async (id: number): Promise<void> => {
    await api.delete(`/plants/${id}`)
  },

  // Regar una planta
  water: async (id: number): Promise<void> => {
    await api.post(`/plants/${id}/water`)
  },

  // upload image plant
  uploadImage: async (id: number, image: File): Promise<void> => {
    const formData = new FormData()
    formData.append("image_url", image)
    await api.post(`/plants/${id}/image`, formData)
  },

  getImage: (image_url: string): string => {
    return (image_url !== "") ? API_ORIGIN + image_url : "/plant-placeholder.svg";
  } 
}
