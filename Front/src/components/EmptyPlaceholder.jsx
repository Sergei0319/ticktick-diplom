/**
 * Заглушка, когда список пуст
 * и показывать нечего.
 */

import { Empty } from "antd";

export function EmptyPlaceholder({ description = "Нет данных" }) {
  return <Empty description={description} style={{ padding: 32 }} />;
}