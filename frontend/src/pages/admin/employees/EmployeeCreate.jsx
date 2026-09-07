import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Input from "../../../components/common/Input";
import Button from "../../../components/common/Button";

function EmployeeCreate() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    employee_code: "",
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    department: "",
    designation: "",
    joining_date: "",
  });

  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();

    setError("");

   
    navigate("/admin/employees");
  }

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Create Employee</h1>
          <p>Add a new employee</p>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <form
        className="form-card"
        onSubmit={handleSubmit}
      >
        <div className="form-grid">
          <Input
            label="Employee Code"
            name="employee_code"
            value={form.employee_code}
            onChange={handleChange}
            required
          />

          <Input
            label="First Name"
            name="first_name"
            value={form.first_name}
            onChange={handleChange}
            required
          />

          <Input
            label="Last Name"
            name="last_name"
            value={form.last_name}
            onChange={handleChange}
            required
          />

          <Input
            label="Email"
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
          />

          <Input
            label="Phone"
            name="phone"
            value={form.phone}
            onChange={handleChange}
          />

          <Input
            label="Department"
            name="department"
            value={form.department}
            onChange={handleChange}
          />

          <Input
            label="Designation"
            name="designation"
            value={form.designation}
            onChange={handleChange}
          />

          <Input
            label="Joining Date"
            type="date"
            name="joining_date"
            value={form.joining_date}
            onChange={handleChange}
          />
        </div>

        <div className="form-actions">
          <Button type="submit">
            Create Employee
          </Button>

          <Button
            type="button"
            className="btn-secondary"
            onClick={() =>
              navigate("/admin/employees")
            }
          >
            Cancel
          </Button>
        </div>
      </form>
    </Layout>
  );
}

export default EmployeeCreate;