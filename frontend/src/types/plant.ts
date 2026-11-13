export interface Plant {
  id: number;
  name: string;
  image_url: string;
  active: boolean;
  updated_at: string;
}

export interface PlantRequest {
  name: string;
}

export interface DashboardPlant {
  id: number;
  name: string;
  image_url: string;
  active: boolean;
  humidity: number | null;
  pin: string | null;
  last_reading: string;
}
