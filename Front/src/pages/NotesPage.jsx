import { Button, Space } from "antd";
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiGet, apiSend } from "../api/client";
import { ErrorMessage } from "../components/ErrorMessage";
import { Loader } from "../components/Loader";
import { NoteList } from "../components/NoteList";
import { PageTitle } from "../components/PageTitle";
import { SearchBar } from "../components/SearchBar";
import { TagChips } from "../components/TagChips";
import { TrashDrawer } from "../components/TrashDrawer";

export function NotesPage() {
  const nav = useNavigate();
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [q, setQ] = useState("");
  const [searchHits, setSearchHits] = useState([]);
  const [tag, setTag] = useState(null);
  const [trashOpen, setTrashOpen] = useState(false);
  const [trash, setTrash] = useState([]);

  async function load() {
    setLoading(true);
    try {
      const url = tag ? `/api/notes?tag=${encodeURIComponent(tag)}` : "/api/notes";
      setNotes(await apiGet(url));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [tag]);

  useEffect(() => {
    if (!q.trim()) {
      setSearchHits([]);
      return;
    }
    const t = setTimeout(async () => {
      try {
        setSearchHits(await apiGet(`/api/notes/search?q=${encodeURIComponent(q)}`));
      } catch {
        setSearchHits([]);
      }
    }, 300);
    return () => clearTimeout(t);
  }, [q]);

  const allTags = useMemo(() => {
    const s = new Set();
    notes.forEach((n) => n.tags?.forEach((t) => s.add(t)));
    return [...s].sort();
  }, [notes]);

  async function createNote() {
    const note = await apiSend("POST", "/api/notes", { title: "Новая заметка", content: "", tags: [] });
    nav(`/notes/${note.id}`);
  }

  async function openTrash() {
    setTrash(await apiGet("/api/notes/trash"));
    setTrashOpen(true);
  }

  if (loading && !q) return <Loader />;
  const list = q.trim() ? searchHits : notes;

  return (
    <div>
      <PageTitle
        title="Заметки"
        extra={
          <Space>
            <Button onClick={openTrash}>Корзина</Button>
            <Button type="primary" onClick={createNote}>
              + Заметка
            </Button>
          </Space>
        }
      />
      <ErrorMessage message={error} onClose={() => setError(null)} />
      <SearchBar value={q} onChange={setQ} />
      <TagChips tags={allTags} active={tag} onSelect={setTag} />
      <NoteList items={list} isSearch={!!q.trim()} />
      <TrashDrawer
        open={trashOpen}
        items={trash}
        onClose={() => setTrashOpen(false)}
        onRestore={async (id) => {
          await apiSend("POST", `/api/notes/${id}/restore`);
          setTrash((t) => t.filter((n) => n.id !== id));
          load();
        }}
        onDelete={async (id) => {
          await apiSend("DELETE", `/api/notes/${id}/permanent`);
          setTrash((t) => t.filter((n) => n.id !== id));
        }}
      />
    </div>
  );
}