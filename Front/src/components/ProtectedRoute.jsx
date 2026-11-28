import { Navigate, useLocation } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

// Доступ только для вошедших пользователей
export function ProtectedRoute({ children }) {
  const token = useAuthStore((s) => s.accessToken);
  const location = useLocation();
  if (!token) return <Navigate to="/auth/login" state={{ from: location }} replace />;
  return children;
}
