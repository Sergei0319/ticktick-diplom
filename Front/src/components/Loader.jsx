/**
 * Индикатор ожидания, пока страница
 * получает данные с сервера.
 */

import { Spin } from "antd";

export function Loader({ tip = "Загрузка..." }) {
  return (
    <div style={{ textAlign: "center", padding: 48 }}>
      <Spin size="large" tip={tip} />
    </div>
  );
}