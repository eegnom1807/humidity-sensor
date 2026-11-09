import api, { API_ORIGIN } from "./api"
import type {
  Plant, 
  PlantRequest, 
  PlantResponse, 
  PlantsResponse, 
  DashboardPlant, 
  DashboardPlantsResponse, 
  PlantRequestUpdate 
} from "@/types/plant"

export const plantService = {
  // Get dashboard data
  getDashboard: async (): Promise<DashboardPlant[]> => {
    const response = await api.get<DashboardPlantsResponse>("/plants/dashboard");
    return response.data.data;
  },

  // Get all plants
  getAll: async (): Promise<Plant[]> => {
    const response = await api.get<PlantsResponse>("/plants");
    return response.data.data;
  },

  // Create plant
  create: async (data: PlantRequest): Promise<Plant> => {
    const response = await api.post<PlantResponse>("/plants", data)
    return response.data.data
  },

  // Update plant
  update: async (id: number, data: PlantRequestUpdate): Promise<Plant> => {
    const response = await api.put<PlantResponse>(`/plants/${id}`, data)
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
  uploadImage: async (id: number, formData: FormData): Promise<void> => {
    await api.post(`/plants/${id}/image`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },

  getImage: (image_url: string): string => {
    return (image_url !== "") ? API_ORIGIN + image_url : "/plant-placeholder.svg";
  } 
}

export default plantService
