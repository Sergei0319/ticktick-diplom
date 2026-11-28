import { Spin } from "antd";

// Индикатор загрузки
export function Loader({ tip = "Загрузка..." }) {
  return (
    <div style={{ textAlign: "center", padding: 48 }}>
      <Spin size="large" tip={tip} />
    </div>
  );
}
