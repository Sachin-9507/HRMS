import { useParams } from "react-router-dom";

import Layout from "../../../components/layout/Layout";

function RoleEdit() {
  const { roleId } = useParams();

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Role Permissions</h1>
          <p>Role ID: {roleId}</p>
        </div>
      </div>

      <div className="form-card">
        Permission assignment will be connected to
        the backend in Part 34.
      </div>
    </Layout>
  );
}

export default RoleEdit;