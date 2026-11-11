import { useEffect, useState } from "react"
import { Plus, Pencil, Trash2, Leaf } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { ConfirmDialog } from "@/components/ConfirmDialog"
import { PlantForm } from "@/components/PlantForm"
import type { Plant, PlantRequest, PlantRequestUpdate } from "@/types/plant"
import plantService from "@/services/plantService";
import { getApiErrorMessage, toastMessage } from "@/lib/utils"

export function Plants() {
  const [formOpen, setFormOpen] = useState(false)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [selectedPlant, setSelectedPlant] = useState<Plant | null>(null)
  const [plants, setPlants] = useState<Plant[]>([]);
  const [error, setError] = useState('');

  const getAllPlants = () => {
    return plantService.getAll()
      .then((response) => {
        setPlants(response);
        setError('');
      })
      .catch((error) => {
        if (error instanceof Error) {
          const errorMsg = `Error al cargar las plantas: ${error.message}`;
          console.error(errorMsg);
          setError(errorMsg);
        }
      })
  }

  useEffect(() => {
    getAllPlants();
  }, [])

  const handleCreate = () => {
    setSelectedPlant(null)
    setFormOpen(true)
  }

  const handleEdit = (plant: Plant) => {
    setSelectedPlant(plant)
    setFormOpen(true)
  }

  const handleDelete = (plant: Plant) => {
    setSelectedPlant(plant)
    setDeleteDialogOpen(true)
  }

  const handleFormSubmit = async (data: PlantRequest, edit: boolean, image?: File) => {
    let plantId = data.id;

    try {
      if (!edit) {
        const plant = await plantService.create(data);
        plantId = plant.id;
        toastMessage("Planta creada", "success");
      } else if (data.id) {
        const new_data: PlantRequestUpdate = {
          name: data.name
        }
        await plantService.update(data.id, new_data);
        toastMessage("Planta actualizada", "success");
      }
    } catch (error) {
      const fallback = edit ? "Error al actualizar la planta" : "Error al crear la planta";
      toastMessage(getApiErrorMessage(error, fallback), "error");
      return;
    }

    if (image && plantId) {
      try {
        const formData = new FormData()
        formData.append("image_url", image);
        await plantService.uploadImage(plantId, formData);
      } catch (error) {
        const reason = getApiErrorMessage(error, "Error al subir la imagen");
        toastMessage(`La planta se guardó, pero falta la imagen: ${reason}`, "error");
      }
    }

    setFormOpen(false);
    getAllPlants();
  }

  const handleConfirmDelete = async () => {
    if (!selectedPlant) return;

    try {
      await plantService.delete(selectedPlant.id);
      toastMessage("Planta eliminada", "success");
      getAllPlants();
    } catch (error) {
      toastMessage(getApiErrorMessage(error, "Error al eliminar la planta"), "error");
    }

    setDeleteDialogOpen(false)
    setSelectedPlant(null)
  }

  const isActive = (active: boolean): string => {
    return (active) ? "Sí" : "No";
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Leaf className="h-8 w-8 text-green-600" />
          <h1 className="text-3xl font-bold">Plantas</h1>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="mr-2 h-4 w-4" />
          Agregar
        </Button>
      </div>

      <div className="overflow-x-auto rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-20">Imagen</TableHead>
              <TableHead>Nombre</TableHead>
              <TableHead>Activa</TableHead>
              <TableHead>Fecha de modificación</TableHead>
              <TableHead className="w-25">Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {plants.map((plant) => (
              <TableRow key={plant.id}>
                <TableCell>
                  <img
                    src={plantService.getImage(plant.image_url)}
                    alt={plant.name}
                    className="h-12 w-12 rounded-md object-cover"
                  />
                </TableCell>
                <TableCell className="font-medium">{plant.name}</TableCell>
                <TableCell className="font-medium">{isActive(plant.active)}</TableCell>
                <TableCell className="font-medium">{plant.updated_at}</TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleEdit(plant)}
                    >
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleDelete(plant)}
                    >
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
            {plants.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center">
                  No hay plantas registradas.
                </TableCell>
              </TableRow>
            )}
            {error && (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center text-red-600">
                  {error}
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <PlantForm
        open={formOpen}
        onOpenChange={setFormOpen}
        plant={selectedPlant}
        onSubmit={handleFormSubmit}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        title="Eliminar Planta"
        description={`¿Estás seguro de que deseas eliminar "${selectedPlant?.name ?? ""}"?`}
        onConfirm={handleConfirmDelete}
      />
    </div>
  )
}
