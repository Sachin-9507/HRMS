import { useParams } from "react-router-dom";

import Layout from "../../../components/layout/Layout";

function UserEdit() {
  const { userId } = useParams();

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Edit User</h1>
          <p>User ID: {userId}</p>
        </div>
      </div>

      <div className="form-card">
        User editing will be connected to the backend
        in Part 34.
      </div>
    </Layout>
  );
}

export default UserEdit;