/**
 * Это цветные наклейки-теги; нажал — покажут только заметки с этим тегом.
 * Ещё раз нажал — фильтр снимается.
 * Как сортировка книг по цвету корешка.
 */
import { Tag } from "antd";

export function TagChips({ tags, active, onSelect }) {
  if (!tags?.length) return null;
  return (
    <div style={{ marginBottom: 16 }}>
      {tags.map((t) => (
        <Tag
          key={t}
          color={active === t ? "blue" : "default"}
          style={{ cursor: "pointer" }}
          onClick={() => onSelect(t === active ? null : t)}
        >
          #{t}
        </Tag>
      ))}
    </div>
  );
}