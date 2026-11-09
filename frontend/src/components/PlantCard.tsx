import { Droplets, CalendarDays, Circle } from "lucide-react"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { DashboardPlant } from "@/types/plant"
import plantService from "@/services/plantService"

interface PlantCardProps {
  plant: DashboardPlant
  onWater?: (pin: string) => void
}

export function PlantCard({ plant, onWater }: PlantCardProps) {
  const hasReadings = plant.humidity != null && plant.last_reading !== ""

  return (
    <Card className={`overflow-hidden${!hasReadings ? " opacity-50 pointer-events-none" : ""}`}>
      <div className="aspect-square w-full overflow-hidden">
        <img
          src={plantService.getImage(plant.image_url)}
          alt={plant.name}
          className="h-full w-full object-cover transition-transform hover:scale-105"
        />
      </div>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{plant.name}</CardTitle>
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Circle className={`h-2.5 w-2.5 fill-current ${plant.active ? "text-green-500" : "text-red-500"}`} />
            <span>{plant.active ? "Activa" : "Inactiva"}</span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Droplets className="h-4 w-4 text-blue-500" />
          <span>Humedad: {plant.humidity != null ? `${plant.humidity}%` : "Sin datos"}</span>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <CalendarDays className="h-4 w-4" />
          <span>Lectura: {plant.last_reading || "Sin lectura"}</span>
        </div>
      </CardContent>
      <CardFooter>
        <Button
          className="w-full"
          disabled={!hasReadings}
          onClick={() => onWater?.(plant.pin)}
        >
          <Droplets className="mr-2 h-4 w-4" />
          Regar Planta
        </Button>
      </CardFooter>
    </Card>
  )
}
