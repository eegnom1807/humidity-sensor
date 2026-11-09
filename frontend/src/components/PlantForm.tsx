import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import type { Plant, PlantRequest } from "@/types/plant"

interface PlantFormProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  plant?: Plant | null
  onSubmit?: (data: PlantRequest, edit: boolean, image?: File) => Promise<void>
}

export function PlantForm({ open, onOpenChange, plant, onSubmit }: PlantFormProps) {
  const isEditing = !!plant
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const data: PlantRequest = {
      name: formData.get("name") as string,
      image_url: "",
    }
    if (isEditing && plant) {
      data.id = plant.id
    }
    const imageFile = formData.get("image_url") as File | null

    setSubmitting(true)
    try {
      await onSubmit?.(data, isEditing, imageFile && imageFile.size > 0 ? imageFile : undefined)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-106.25">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar Planta" : "Agregar Planta"}
          </DialogTitle>
          <DialogDescription>
            {isEditing
              ? "Modifica los datos de tu planta."
              : "Agrega una nueva planta a tu colección."}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="name">Nombre</Label>
              <Input
                id="name"
                name="name"
                placeholder="Ej: Planta de tomate"
                defaultValue={plant?.name ?? ""}
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="image_url">Imagen</Label>
              <Input
                id="image_url"
                name="image_url"
                type="file"
                accept="image/png, image/jpeg"
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancelar
            </Button>
            <Button type="submit" disabled={submitting}>
              {isEditing ? "Guardar Cambios" : "Crear Planta"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
