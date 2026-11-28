import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

// Доступ только для роли admin
export function AdminRoute({ children }) {
  const role = useAuthStore((s) => s.role);
  if (role !== "admin") return <Navigate to="/" replace />;
  return children;
}
