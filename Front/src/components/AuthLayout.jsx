import { Card, Typography } from "antd";

// Каркас страниц входа и регистрации
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
