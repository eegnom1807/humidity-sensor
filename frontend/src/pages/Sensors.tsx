import { useEffect, useState } from "react"
import { Plus, Pencil, Trash2, Cpu } from "lucide-react"
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
import { SensorForm } from "@/components/SensorForm"
import type { Sensor, SensorRequest } from "@/types/sensor"
import type { Plant } from "@/types/plant"
import sensorService from "@/services/sensorService"
import plantService from "@/services/plantService";
import { getApiErrorMessage, toastMessage } from "@/lib/utils"

export function Sensors() {
  const [formOpen, setFormOpen] = useState(false)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [selectedSensor, setSelectedSensor] = useState<Sensor | null>(null)
  const [sensors, setSensors] = useState<Sensor[]>([])
  const [plants, setPlants] = useState<Plant[]>([])
  const [errorPlants, setErrorPlants] = useState('');
  const [errorSensors, setErrorSensors] = useState('');

  const getAllSensors = () => {
    return sensorService.getAll()
      .then((response) => {
        setSensors(response);
        setErrorSensors('');
      })
      .catch((error) => {
        if (error instanceof Error) {
          const errorMsg = `Error al cargar los sensores: ${error.message}`;
          console.error(errorMsg);
          setErrorSensors(errorMsg);
        }
      })
  }

  const getAllPlants = () => {
    return plantService.getAll()
      .then((response) => {
        setPlants(response);
        setErrorPlants('');
      })
      .catch((error) => {
        if (error instanceof Error) {
          const errorMsg = `Error al cargar las plantas: ${error.message}`;
          console.error(errorMsg);
          setErrorPlants(errorMsg);
        }
      })
  };

  useEffect(() => {
    getAllSensors();
    getAllPlants();
  }, [])

  const getPlantName = (plantId: number): string => {
    const plant = plants.find((p) => p.id === plantId)
    return plant?.name ?? String(plantId)
  }

  const handleCreate = () => {
    setSelectedSensor(null)
    setFormOpen(true)
  }

  const handleEdit = (sensor: Sensor) => {
    setSelectedSensor(sensor)
    setFormOpen(true)
  }

  const handleDelete = (sensor: Sensor) => {
    setSelectedSensor(sensor)
    setDeleteDialogOpen(true)
  }

  const handleFormSubmit = async (data: SensorRequest, edit: boolean) => {
    try {
      if (!edit) {
        await sensorService.create(data)
        toastMessage("Sensor creado", "success");
      } else if (selectedSensor) {
        await sensorService.update(selectedSensor.id, data)
        toastMessage("Sensor actualizado", "success");
      }

      setFormOpen(false)
      getAllSensors()
    } catch (error) {
      const fallback = edit ? "Error al actualizar el sensor" : "Error al crear el sensor";
      toastMessage(getApiErrorMessage(error, fallback), "error");
    }
  }

  const handleConfirmDelete = async () => {
    if (!selectedSensor) return;

    try {
      await sensorService.delete(selectedSensor.id)
      toastMessage("Sensor eliminado", "success");
      getAllSensors()
    } catch (error) {
      toastMessage(getApiErrorMessage(error, "Error al eliminar el sensor"), "error");
    }

    setDeleteDialogOpen(false)
    setSelectedSensor(null)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Cpu className="h-8 w-8 text-green-600" />
          <h1 className="text-3xl font-bold">Sensores</h1>
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
              <TableHead>Pin</TableHead>
              <TableHead>Planta</TableHead>
              <TableHead>Fecha de modificación</TableHead>
              <TableHead className="w-25">Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sensors.map((sensor) => (
              <TableRow key={sensor.id}>
                <TableCell className="font-medium">{sensor.pin}</TableCell>
                <TableCell className="font-medium">{getPlantName(sensor.plant_id)}</TableCell>
                <TableCell className="font-medium">{sensor.updated_at}</TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleEdit(sensor)}
                    >
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleDelete(sensor)}
                    >
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
            {sensors.length === 0 && (
              <TableRow>
                <TableCell colSpan={4} className="h-24 text-center">
                  No hay sensores registrados.
                </TableCell>
              </TableRow>
            )}
            {(errorSensors || errorPlants) && (
              <TableRow>
                <TableCell colSpan={4} className="h-24 text-center">
                  {errorSensors && (
                    <div className="text-red-500">{errorSensors}</div>
                  )}
                  {errorPlants && (
                    <div className="text-red-500">{errorPlants}</div>
                  )}
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <SensorForm
        open={formOpen}
        onOpenChange={setFormOpen}
        sensor={selectedSensor}
        onSubmit={handleFormSubmit}
        plants={plants}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        title="Eliminar Sensor"
        description={`¿Estás seguro de que deseas eliminar el sensor "${selectedSensor?.pin ?? ""}"?`}
        onConfirm={handleConfirmDelete}
      />
    </div>
  )
}
