export interface Plant {
  id: number;
  name: string;
  image_url: string;
  active: boolean;
  updated_at: string;
}

export interface PlantRequest {
  id?: number;
  name: string;
}

export interface PlantRequestUpdate {
  name: string;
}

export interface DashboardPlant {
  id: number;
  name: string;
  image_url: string;
  active: boolean;
  humidity: number | null;
  pin: string;
  last_reading: string;
}

export interface PlantsResponse {
  data: Plant[];
}

export interface DashboardPlantsResponse {
  data: DashboardPlant[];
}

export interface PlantResponse {
  data: Plant;
}