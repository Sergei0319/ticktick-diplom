/**
 * Это строка поиска, как в библиотеке.
 * Набираешь слово, нажимаешь Enter — родитель ищет на сервере.
 * Сам по себе поиск не делает — только поле ввода.
 */
import { Input } from "antd";

export function SearchBar({ value, onChange, placeholder = "Поиск..." }) {
  return <Input.Search allowClear placeholder={placeholder} value={value} onChange={(e) => onChange(e.target.value)} />;
}