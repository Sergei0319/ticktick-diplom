/**
 * Это красная плашка «что-то пошло не так».
 * Показывает текст ошибки от сервера простыми словами.
 * Можно закрыть крестиком и попробовать снова.
 */
import { Alert } from "antd";

export function ErrorMessage({ message, onClose }) {
  if (!message) return null;
  return <Alert type="error" message={message} closable onClose={onClose} style={{ marginBottom: 16 }} />;
}