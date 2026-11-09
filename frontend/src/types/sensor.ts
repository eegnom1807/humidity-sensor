export interface Sensor {
  id: number
  pin: string
  plant_id: number
  updated_at: string
}

export interface SensorRequest {
  pin: string
  plant_id: number
}

export interface SensorsResponse {
  data: Sensor[]
}

export interface SensorResponse {
  data: Sensor
}
