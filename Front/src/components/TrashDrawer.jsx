/**
 * Это выдвижной ящик «корзина» с удалёнными заметками.
 * Можно вернуть заметку или стереть навсегда.
 * Выезжает сбоку, как ящик стола.
 */
import { Button, Drawer, List, Space } from "antd";

export function TrashDrawer({ open, items, onClose, onRestore, onDelete }) {
  return (
    <Drawer title="Корзина" open={open} onClose={onClose} width={420}>
      <List
        dataSource={items}
        locale={{ emptyText: "Корзина пуста" }}
        renderItem={(item) => (
          <List.Item
            actions={[
              <Button key="r" size="small" onClick={() => onRestore(item.id)}>
                Восстановить
              </Button>,
              <Button key="d" size="small" danger onClick={() => onDelete(item.id)}>
                Удалить
              </Button>,
            ]}
          >
            {item.title}
          </List.Item>
        )}
      />
    </Drawer>
  );
}