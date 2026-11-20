/**
 * Это охранник: без билетика (токена) не пустит внутрь приложения.
 * Отправит на login и запомнит, куда ты хотел попасть.
 * Оборачивает все страницы, кроме /auth.
 */
import { Navigate, useLocation } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export function ProtectedRoute({ children }) {
  const token = useAuthStore((s) => s.accessToken);
  const location = useLocation();
  if (!token) return <Navigate to="/auth/login" state={{ from: location }} replace />;
  return children;
}