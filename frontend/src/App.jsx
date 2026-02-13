import { Routes, Route, Navigate } from 'react-router-dom'
import { SetupProvider, useSetup } from './context/SetupContext'
import Layout from './components/Layout'
import LoadingSpinner from './components/LoadingSpinner'

import SetupWizard from './pages/setup/SetupWizard'
import DashboardPage from './pages/dashboard/DashboardPage'
import HouseListPage from './pages/houses/HouseListPage'
import HouseFormPage from './pages/houses/HouseFormPage'
import HouseDetailPage from './pages/houses/HouseDetailPage'
import RoomFormPage from './pages/rooms/RoomFormPage'
import DeviceFormPage from './pages/devices/DeviceFormPage'
import ScheduleListPage from './pages/schedules/ScheduleListPage'
import ScheduleFormPage from './pages/schedules/ScheduleFormPage'
import SettingsPage from './pages/settings/SettingsPage'

function AppRoutes() {
  const { setupComplete, checking } = useSetup()

  if (checking) return <LoadingSpinner text="Checking setup status..." />

  if (!setupComplete) {
    return (
      <Routes>
        <Route path="/setup" element={<SetupWizard />} />
        <Route path="*" element={<Navigate to="/setup" replace />} />
      </Routes>
    )
  }

  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/houses" element={<HouseListPage />} />
        <Route path="/houses/new" element={<HouseFormPage />} />
        <Route path="/houses/:id" element={<HouseDetailPage />} />
        <Route path="/houses/:id/edit" element={<HouseFormPage />} />
        <Route path="/houses/:id/rooms/new" element={<RoomFormPage />} />
        <Route path="/houses/:id/rooms/:roomId/edit" element={<RoomFormPage />} />
        <Route path="/houses/:id/rooms/:roomId/schedules" element={<ScheduleListPage />} />
        <Route path="/houses/:id/rooms/:roomId/schedules/new" element={<ScheduleFormPage />} />
        <Route path="/houses/:id/devices/new" element={<DeviceFormPage />} />
        <Route path="/devices/:deviceId/edit" element={<DeviceFormPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/setup" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}

export default function App() {
  return (
    <SetupProvider>
      <AppRoutes />
    </SetupProvider>
  )
}
