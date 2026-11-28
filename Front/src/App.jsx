import { Navigate, Route, Routes } from "react-router-dom";
import { AdminRoute } from "./components/AdminRoute";
import { AppLayout } from "./components/AppLayout";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { AdminPage } from "./pages/AdminPage";
import { CalendarPage } from "./pages/CalendarPage";
import { HomePage } from "./pages/HomePage";
import { LoginPage } from "./pages/LoginPage";
import { NoteDetailPage } from "./pages/NoteDetailPage";
import { NotesPage } from "./pages/NotesPage";
import { ProfilePage } from "./pages/ProfilePage";
import { RegisterPage } from "./pages/RegisterPage";
import { TodosPage } from "./pages/TodosPage";
import { useAuthStore } from "./store/authStore";

// Страницы входа: если токен есть, уводит на главную
function GuestOnly({ children }) {
  const token = useAuthStore((s) => s.accessToken);
  if (token) return <Navigate to="/" replace />;
  return children;
}

// Карта адресов приложения
export function App() {
  return (
    <Routes>
      <Route path="/auth/login" element={<GuestOnly><LoginPage /></GuestOnly>} />
      <Route path="/auth/register" element={<GuestOnly><RegisterPage /></GuestOnly>} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<HomePage />} />
        <Route path="notes" element={<NotesPage />} />
        <Route path="notes/:id" element={<NoteDetailPage />} />
        <Route path="calendar" element={<CalendarPage />} />
        <Route path="todos" element={<TodosPage />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route
          path="admin"
          element={
            <AdminRoute>
              <AdminPage />
            </AdminRoute>
          }
        />
      </Route>
    </Routes>
  );
}
