import { Navigate, Route, Routes } from 'react-router-dom'
import LoginPage from '../pages/auth/LoginPage'
import AdminDashboard from '../pages/admin/AdminDashboard'
import UsersPage from '../pages/admin/UsersPage'
import ClientsPage from '../pages/admin/ClientsPage'
import TreatmentsPage from '../pages/admin/TreatmentsPage'
import CalendarPage from '../pages/admin/CalendarPage'
import WorkerDashboard from '../pages/worker/WorkerDashboard'
import WorkerAgendaPage from '../pages/worker/WorkerAgendaPage'
import WorkerClinicalPage from '../pages/worker/WorkerClinicalPage'
import ClientDashboard from '../pages/client/ClientDashboard'
import ClientProfilePage from '../pages/client/ClientProfilePage'
import ClientAppointmentsPage from '../pages/client/ClientAppointmentsPage'
import ClientTreatmentsPage from '../pages/client/ClientTreatmentsPage'
import ClientPrivacyPage from '../pages/client/ClientPrivacyPage'
import NotFoundPage from '../pages/misc/NotFoundPage'
import UnauthorizedPage from '../pages/misc/UnauthorizedPage'
import { useRoleGuard } from '../hooks/useRoleGuard'

const PrivateRoute = ({ roles, children }: { roles: string[]; children: JSX.Element }) => {
  const { user, allowed } = useRoleGuard(roles)
  if (user === null) return <Navigate to="/login" />
  if (!allowed) return <UnauthorizedPage />
  return children
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/admin"
        element={
          <PrivateRoute roles={["admin"]}>
            <AdminDashboard />
          </PrivateRoute>
        }
      />
      <Route
        path="/admin/users"
        element={
          <PrivateRoute roles={["admin"]}>
            <UsersPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/admin/clients"
        element={
          <PrivateRoute roles={["admin", "worker"]}>
            <ClientsPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/admin/treatments"
        element={
          <PrivateRoute roles={["admin"]}>
            <TreatmentsPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/admin/calendar"
        element={
          <PrivateRoute roles={["admin"]}>
            <CalendarPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/worker"
        element={
          <PrivateRoute roles={["worker"]}>
            <WorkerDashboard />
          </PrivateRoute>
        }
      />
      <Route
        path="/worker/agenda"
        element={
          <PrivateRoute roles={["worker"]}>
            <WorkerAgendaPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/worker/clinical"
        element={
          <PrivateRoute roles={["worker"]}>
            <WorkerClinicalPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/client"
        element={
          <PrivateRoute roles={["client"]}>
            <ClientDashboard />
          </PrivateRoute>
        }
      />
      <Route
        path="/client/profile"
        element={
          <PrivateRoute roles={["client"]}>
            <ClientProfilePage />
          </PrivateRoute>
        }
      />
      <Route
        path="/client/privacy"
        element={
          <PrivateRoute roles={["client"]}>
            <ClientPrivacyPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/client/appointments"
        element={
          <PrivateRoute roles={["client"]}>
            <ClientAppointmentsPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/client/treatments"
        element={
          <PrivateRoute roles={["client"]}>
            <ClientTreatmentsPage />
          </PrivateRoute>
        }
      />
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default AppRoutes
