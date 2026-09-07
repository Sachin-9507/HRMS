import { Link } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Table from "../../../components/common/Table";

function RoleList() {
  const roles = [];

  const columns = [
    {
      key: "id",
      label: "ID",
    },
    {
      key: "name",
      label: "Role Name",
    },
    {
      key: "description",
      label: "Description",
    },
    {
      key: "actions",
      label: "Actions",
      render: (row) => (
        <Link
          to={`/admin/roles/${row.id}/edit`}
          className="table-action"
        >
          Manage Permissions
        </Link>
      ),
    },
  ];

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Roles</h1>
          <p>Manage system roles</p>
        </div>
      </div>

      <Table
        columns={columns}
        data={roles}
        emptyMessage="No roles found"
      />
    </Layout>
  );
}

export default RoleList;