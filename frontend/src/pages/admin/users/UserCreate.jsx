import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Input from "../../../components/common/Input";
import Button from "../../../components/common/Button";

function UserCreate() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
    employee_id: "",
    role_id: "",
  });

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();

    // Backend integration comes in Part 34.

    navigate("/admin/users");
  }

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Create User</h1>
          <p>Create a new HRMS login account</p>
        </div>
      </div>

      <form
        className="form-card"
        onSubmit={handleSubmit}
      >
        <Input
          label="Email"
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          required
        />

        <Input
          label="Password"
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          required
        />

        <Input
          label="Employee ID"
          type="number"
          name="employee_id"
          value={form.employee_id}
          onChange={handleChange}
        />

        <Input
          label="Role ID"
          type="number"
          name="role_id"
          value={form.role_id}
          onChange={handleChange}
        />

        <div className="form-actions">
          <Button type="submit">
            Create User
          </Button>

          <Button
            type="button"
            className="btn-secondary"
            onClick={() =>
              navigate("/admin/users")
            }
          >
            Cancel
          </Button>
        </div>
      </form>
    </Layout>
  );
}

export default UserCreate;