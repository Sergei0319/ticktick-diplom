/**
 * Заголовок экрана и место справа
 * для кнопок этого экрана.
 */

import { Typography } from "antd";

export function PageTitle({ title, extra }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
      <Typography.Title level={3} style={{ margin: 0 }}>
        {title}
      </Typography.Title>
      {extra}
    </div>
  );
}