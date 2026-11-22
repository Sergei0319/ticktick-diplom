/**
 * Экран задач.
 * Показывает список, создаёт задачу с приоритетом,
 * отмечает выполнение и удаляет её.
 */

import { useEffect, useState } from "react";
import { apiGet, apiSend } from "../api/client";
import { ErrorMessage } from "../components/ErrorMessage";
import { Loader } from "../components/Loader";
import { PageTitle } from "../components/PageTitle";
import { TodoCreateForm } from "../components/TodoCreateForm";
import { TodoItem } from "../components/TodoItem";

export function TodosPage() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState(2);

  async function load() {
    setLoading(true);
    try {
      setTodos(await apiGet("/api/todos"));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (loading) return <Loader />;

  return (
    <div>
      <PageTitle title="Задачи" />
      <ErrorMessage message={error} onClose={() => setError(null)} />
      <TodoCreateForm
        title={title}
        priority={priority}
        onTitle={setTitle}
        onPriority={setPriority}
        onSubmit={async () => {
          if (!title.trim()) return;
          await apiSend("POST", "/api/todos", { title, priority });
          setTitle("");
          load();
        }}
      />
      {todos.map((t) => (
        <TodoItem
          key={t.id}
          todo={t}
          onToggle={async (id) => {
            await apiSend("PATCH", `/api/todos/${id}/toggle`);
            load();
          }}
          onDelete={async (id) => {
            await apiSend("DELETE", `/api/todos/${id}`);
            load();
          }}
        />
      ))}
    </div>
  );
}