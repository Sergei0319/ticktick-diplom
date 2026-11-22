/**
 * Поле ввода строки поиска.
 * Само ничего не запрашивает,
 * только передаёт текст родителю.
 */

import { Input } from "antd";

export function SearchBar({ value, onChange, placeholder = "Поиск..." }) {
  return <Input.Search allowClear placeholder={placeholder} value={value} onChange={(e) => onChange(e.target.value)} />;
}