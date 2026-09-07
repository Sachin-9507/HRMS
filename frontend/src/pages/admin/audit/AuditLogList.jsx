import Layout from "../../../components/layout/Layout";
import Table from "../../../components/common/Table";
import Badge from "../../../components/common/Badge";

function AuditLogList() {
  const logs = [];

  const columns = [
    {
      key: "id",
      label: "ID",
    },
    {
      key: "user_id",
      label: "User",
    },
    {
      key: "action",
      label: "Action",
    },
    {
      key: "module",
      label: "Module",
    },
    {
      key: "entity_type",
      label: "Entity",
    },
    {
      key: "status",
      label: "Status",
      render: (row) => (
        <Badge status={row.status} />
      ),
    },
    {
      key: "created_at",
      label: "Created At",
    },
  ];

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Audit Logs</h1>
          <p>System activity and audit history</p>
        </div>
      </div>

      <Table
        columns={columns}
        data={logs}
        emptyMessage="No audit logs found"
      />
    </Layout>
  );
}

export default AuditLogList;