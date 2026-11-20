/**
 * Это одна карточка заметки на полке: название, теги, клик — открыть.
 * Как этикетка на папке в шкафу.
 * Самa данные не качает — получает от NotesPage.
 */
import { Card, Tag } from "antd";
import { Link } from "react-router-dom";

export function NoteCard({ note, snippet }) {
  return (
    <Link to={`/notes/${note.id}`}>
      <Card size="small" hoverable style={{ marginBottom: 12 }}>
        <strong>{note.title}</strong>
        {snippet && <div style={{ color: "#666", marginTop: 8 }}>{snippet}</div>}
        <div style={{ marginTop: 8 }}>
          {(note.tags || []).map((t) => (
            <Tag key={t}>{t}</Tag>
          ))}
        </div>
      </Card>
    </Link>
  );
}