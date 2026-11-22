/**
 * Одна задача в списке.
 * Показывает приоритет и даёт отметить
 * её выполненной или удалить.
 */

import { Button, Card, Checkbox, Tag } from "antd";

const pri = { 1: "Высокий", 2: "Средний", 3: "Низкий" };
const colors = { 1: "red", 2: "orange", 3: "default" };

export function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <Card size="small" style={{ marginBottom: 12, opacity: todo.isDone ? 0.65 : 1 }}>
      <Checkbox checked={todo.isDone} onChange={() => onToggle(todo.id)}>
        <span style={{ textDecoration: todo.isDone ? "line-through" : "none" }}>{todo.title}</span>
      </Checkbox>
      <div style={{ marginTop: 8 }}>
        <Tag color={colors[todo.priority]}>{pri[todo.priority]}</Tag>
        {todo.dueAt && <Tag>{new Date(todo.dueAt).toLocaleString("ru")}</Tag>}
      </div>
      <Button danger size="small" style={{ marginTop: 8 }} onClick={() => onDelete(todo.id)}>
        Удалить
      </Button>
    </Card>
  );
}