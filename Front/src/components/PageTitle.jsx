import { Typography } from "antd";

// Заголовок страницы и кнопки справа
export function PageTitle({ title, extra }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
      <Typography.Title level={3} style={{ margin: 0 }}>
        {title}
      </Typography.Title>
      {extra}
    </div>
  );
}
