import { Card, Descriptions, Tag } from "antd";

// Карточка профиля
export function ProfileCard({ profile }) {
  if (!profile) return null;
  return (
    <Card title="Профиль">
      <Descriptions column={1}>
        <Descriptions.Item label="Email">{profile.email}</Descriptions.Item>
        <Descriptions.Item label="Имя">{profile.displayName || "—"}</Descriptions.Item>
        <Descriptions.Item label="Роль">
          <Tag color={profile.role === "admin" ? "gold" : "blue"}>{profile.role}</Tag>
        </Descriptions.Item>
        <Descriptions.Item label="Регистрация">
          {new Date(profile.createdAt).toLocaleDateString("ru")}
        </Descriptions.Item>
      </Descriptions>
    </Card>
  );
}
