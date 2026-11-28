import { NoteCard } from "./NoteCard";
import { EmptyPlaceholder } from "./EmptyPlaceholder";

// Список карточек заметок
export function NoteList({ items, isSearch }) {
  if (!items?.length) return <EmptyPlaceholder description="Заметок пока нет" />;
  return items.map((n) => <NoteCard key={n.id} note={n} snippet={isSearch ? n.snippet : null} />);
}
