/**
 * Это красивая рамка для login и register — карточка по центру экрана.
 * Чтобы форма не плавала в углу, а выглядела аккуратно.
 * Внутрь кладётся только форма входа или регистрации.
 */
import { Card, Typography } from "antd";

export function AuthLayout({ title, children }) {
  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <Card style={{ width: 400 }}>
        <Typography.Title level={3}>{title}</Typography.Title>
        {children}
      </Card>
    </div>
  );
}