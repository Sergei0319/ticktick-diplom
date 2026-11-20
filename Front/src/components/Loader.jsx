/**
 * Это крутящийся кружок «подожди, грузим».
 * Пока сервер думает, человек видит, что программа не зависла.
 * Одинаковый на всех страницах.
 */
import { Spin } from "antd";

export function Loader({ tip = "Загрузка..." }) {
  return (
    <div style={{ textAlign: "center", padding: 48 }}>
      <Spin size="large" tip={tip} />
    </div>
  );
}