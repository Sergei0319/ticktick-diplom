import { Menu } from "antd";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

const baseItems = [
  { key: "/", label: "Главная" },
  { key: "/notes", label: "Заметки" },
  { key: "/calendar", label: "Календарь" },
  { key: "/todos", label: "Задачи" },
  { key: "/profile", label: "Личный кабинет" },
];

// Боковое меню навигации
export function SideMenu() {
  const nav = useNavigate();
  const loc = useLocation();
  const role = useAuthStore((s) => s.role);
  const items = role === "admin" ? [...baseItems, { key: "/admin", label: "Админ-панель" }] : baseItems;
  const selected = items.find((i) => loc.pathname === i.key || loc.pathname.startsWith(`${i.key}/`))?.key || "/";

  return (
    <Menu
      mode="inline"
      selectedKeys={[selected === "/notes" && loc.pathname.startsWith("/notes/") ? "/notes" : selected]}
      items={items}
      onClick={({ key }) => nav(key)}
      style={{ height: "100%", borderRight: 0 }}
    />
  );
}
