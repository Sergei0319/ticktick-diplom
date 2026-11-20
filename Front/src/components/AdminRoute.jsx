/**
 * Это второй охранник у двери директора.
 * Смотрит роль в Zustand: не admin — на главную.
 * Даже если угадать URL /admin, экран не покажет пульт.
 */
import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export function AdminRoute({ children }) {
  const role = useAuthStore((s) => s.role);
  if (role !== "admin") return <Navigate to="/" replace />;
  return children;
}