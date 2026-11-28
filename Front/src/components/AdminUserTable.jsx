import { Button, Select, Space, Table, Tag } from "antd";

// Таблица пользователей в админке
export function AdminUserTable({ users, loading, onRole, onDelete }) {
  const columns = [
    { title: "Email", dataIndex: "email" },
    { title: "Имя", dataIndex: "displayName", render: (v) => v || "—" },
    {
      title: "Роль",
      dataIndex: "role",
      render: (role, row) => (
        <Select
          value={role}
          style={{ width: 120 }}
          options={[
            { value: "user", label: "user" },
            { value: "admin", label: "admin" },
          ]}
          onChange={(v) => onRole(row.id, v)}
        />
      ),
    },
    {
      title: "Статус",
      dataIndex: "isDeleted",
      render: (d) => (d ? <Tag color="red">Удалён</Tag> : <Tag color="green">Активен</Tag>),
    },
    {
      title: "Действия",
      render: (_, row) => (
        <Space>
          <Button size="small" danger disabled={row.isDeleted} onClick={() => onDelete(row.id)}>
            Блокировать
          </Button>
        </Space>
      ),
    },
  ];
  return <Table rowKey="id" loading={loading} dataSource={users} columns={columns} pagination={{ pageSize: 8 }} />;
}
