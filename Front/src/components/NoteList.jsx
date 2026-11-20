/**
 * Это стопка карточек NoteCard.
 * Если заметок нет — рисует EmptyPlaceholder «здесь пусто».
 * Удобно, чтобы NotesPage не писала один и тот же цикл много раз.
 */
import { NoteCard } from "./NoteCard";
import { EmptyPlaceholder } from "./EmptyPlaceholder";

export function NoteList({ items, isSearch }) {
  if (!items?.length) return <EmptyPlaceholder description="Заметок пока нет" />;
  return items.map((n) => <NoteCard key={n.id} note={n} snippet={isSearch ? n.snippet : null} />);
}