import { Layout, Typography } from "antd";
import { Outlet } from "react-router-dom";
import { SideMenu } from "./SideMenu";

const { Header, Sider, Content } = Layout;

export function AppLayout() {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider breakpoint="lg" collapsedWidth="0" width={220}>
        <div style={{ padding: 16 }}>
          <Typography.Title level={4} style={{ color: "#fff", margin: 0 }}>
            TickTick
          </Typography.Title>
        </div>
        <SideMenu />
      </Sider>
      <Layout>
        <Header style={{ background: "#fff", padding: "0 24px" }}>
          <Typography.Text type="secondary">Веб-приложение для заметок, календаря и задач</Typography.Text>
        </Header>
        <Content style={{ margin: 24, padding: 24, background: "#fff", borderRadius: 8 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}