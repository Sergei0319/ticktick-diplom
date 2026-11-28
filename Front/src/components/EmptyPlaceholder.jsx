import { Empty } from "antd";

// Заглушка при пустом списке
export function EmptyPlaceholder({ description = "Нет данных" }) {
  return <Empty description={description} style={{ padding: 32 }} />;
}
