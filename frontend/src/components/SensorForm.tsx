import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import type { Sensor, SensorRequest } from "@/types/sensor"
import type { Plant } from "@/types/plant"

interface SensorFormProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  sensor?: Sensor | null
  onSubmit?: (data: SensorRequest) => Promise<void>
  plants: Plant[]
  usedPins: string[]
}

// Arduino UNO R4 WiFi analog pins
const ANALOG_PINS = ["A0", "A1", "A2", "A3", "A4", "A5"]

export function SensorForm({ open, onOpenChange, sensor, onSubmit, plants, usedPins }: SensorFormProps) {
  const isEditing = !!sensor
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const data: SensorRequest = {
      pin: formData.get("pin") as string,
      plant_id: Number(formData.get("plant_id")),
    }

    setSubmitting(true)
    try {
      await onSubmit?.(data)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-106.25">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar Sensor" : "Agregar Sensor"}
          </DialogTitle>
          <DialogDescription>
            {isEditing
              ? "Modifica los datos del sensor."
              : "Agrega un nuevo sensor."}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="pin">Pin</Label>
              <select
                id="pin"
                name="pin"
                defaultValue={sensor?.pin ?? ""}
                required
                className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              >
                <option value="">Seleccionar pin</option>
                {ANALOG_PINS.map((pin) => (
                  <option
                    key={pin}
                    value={pin}
                    disabled={usedPins.includes(pin) && pin !== sensor?.pin}
                  >
                    {pin}
                  </option>
                ))}
              </select>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="plant_id">Planta</Label>
              <select
                id="plant_id"
                name="plant_id"
                defaultValue={sensor?.plant_id ?? ""}
                required
                className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              >
                <option value="">Seleccionar planta</option>
                {plants.map((plant) => (
                  <option key={plant.id} value={plant.id}>
                    {plant.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancelar
            </Button>
            <Button type="submit" disabled={submitting}>
              {isEditing ? "Guardar Cambios" : "Crear Sensor"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
