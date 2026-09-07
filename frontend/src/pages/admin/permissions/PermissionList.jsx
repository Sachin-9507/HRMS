import Layout from "../../../components/layout/Layout";
import Table from "../../../components/common/Table";

function PermissionList() {
  const permissions = [];

  const columns = [
    {
      key: "id",
      label: "ID",
    },
    {
      key: "name",
      label: "Permission",
    },
    {
      key: "description",
      label: "Description",
    },
  ];

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Permissions</h1>
          <p>System permissions</p>
        </div>
      </div>

      <Table
        columns={columns}
        data={permissions}
        emptyMessage="No permissions found"
      />
    </Layout>
  );
}

export default PermissionList;