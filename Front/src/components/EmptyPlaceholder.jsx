/**
 * Это картинка «тут пусто, добавь что-нибудь».
 * Когда список пустой, скучно не будет — видно, что это нормально.
 * Ant Design Empty, как заглушка в игре.
 */
import { Empty } from "antd";

export function EmptyPlaceholder({ description = "Нет данных" }) {
  return <Empty description={description} style={{ padding: 32 }} />;
}