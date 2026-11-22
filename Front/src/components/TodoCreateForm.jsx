import { Button, Input, Select, Space } from "antd";

export function TodoCreateForm({ title, priority, onTitle, onPriority, onSubmit }) {
  return (
    <Space.Compact style={{ width: "100%", marginBottom: 16 }}>
      <Input placeholder="Новая задача" value={title} onChange={(e) => onTitle(e.target.value)} />
      <Select
        value={priority}
        onChange={onPriority}
        options={[
          { value: 1, label: "Высокий" },
          { value: 2, label: "Средний" },
          { value: 3, label: "Низкий" },
        ]}
        style={{ width: 120 }}
      />
      <Button type="primary" onClick={onSubmit}>
        Добавить
      </Button>
    </Space.Compact>
  );
}