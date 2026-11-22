/**
 * Редактор одной заметки.
 * Сохраняет заголовок, теги и текст.
 * Скачивает DOCX или PDF и убирает заметку в корзину.
 */

import { Button, Input, Space, message } from "antd";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { apiGet, apiSend, http } from "../api/client";
import { ErrorMessage } from "../components/ErrorMessage";
import { Loader } from "../components/Loader";
import { PageTitle } from "../components/PageTitle";

const { TextArea } = Input;

export function NoteDetailPage() {
  const { id } = useParams();
  const nav = useNavigate();
  const [note, setNote] = useState(null);
  const [tagsText, setTagsText] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const n = await apiGet(`/api/notes/${id}`);
        setNote(n);
        setTagsText((n.tags || []).join(", "));
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  async function save() {
    setSaving(true);
    try {
      const tags = tagsText
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean);
      const updated = await apiSend("PUT", `/api/notes/${id}`, {
        title: note.title,
        content: note.content,
        tags,
      });
      setNote(updated);
      message.success("Сохранено");
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  }

  async function remove() {
    await apiSend("DELETE", `/api/notes/${id}`);
    nav("/notes");
  }

  async function exportFmt(fmt) {
    try {
      const res = await http.get(`/api/notes/${id}/export/${fmt}`, { responseType: "blob" });
      const url = URL.createObjectURL(res.data);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${note.title}.${fmt}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(e.message);
    }
  }

  if (loading) return <Loader />;
  if (!note) return <ErrorMessage message={error || "Не найдено"} />;

  return (
    <div>
      <PageTitle
        title="Редактор заметки"
        extra={
          <Space wrap>
            <Button onClick={() => nav("/notes")}>Назад</Button>
            <Button type="primary" loading={saving} onClick={save}>
              Сохранить
            </Button>
            <Button onClick={() => exportFmt("docx")}>DOCX</Button>
            <Button onClick={() => exportFmt("pdf")}>PDF</Button>
            <Button danger onClick={remove}>
              В корзину
            </Button>
          </Space>
        }
      />
      <ErrorMessage message={error} onClose={() => setError(null)} />
      <Input value={note.title} onChange={(e) => setNote({ ...note, title: e.target.value })} />
      <Input
        style={{ marginTop: 12 }}
        placeholder="Теги через запятую"
        value={tagsText}
        onChange={(e) => setTagsText(e.target.value)}
      />
      <TextArea
        rows={16}
        style={{ marginTop: 12, fontFamily: "monospace" }}
        value={note.content}
        onChange={(e) => setNote({ ...note, content: e.target.value })}
        placeholder="Markdown, wiki: [[Название другой заметки]]"
      />
    </div>
  );
}