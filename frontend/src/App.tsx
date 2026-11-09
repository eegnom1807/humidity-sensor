import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Layout } from "@/components/Layout"
import { Dashboard } from "@/pages/Dashboard"
import { Plants } from "@/pages/Plants"
import { Sensors } from "@/pages/Sensors"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="plants" element={<Plants />} />
          <Route path="sensors" element={<Sensors />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
