import { useNavigate, useParams } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Button from "../../../components/common/Button";

function EmployeeEdit() {
  const { employeeId } = useParams();
  const navigate = useNavigate();

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Edit Employee</h1>
          <p>
            Employee ID: {employeeId}
          </p>
        </div>
      </div>

      <div className="form-card">
        <p>
          Employee edit form will be connected to the
          backend in Part 34.
        </p>

        <Button
          type="button"
          onClick={() =>
            navigate("/admin/employees")
          }
        >
          Back to Employees
        </Button>
      </div>
    </Layout>
  );
}

export default EmployeeEdit;