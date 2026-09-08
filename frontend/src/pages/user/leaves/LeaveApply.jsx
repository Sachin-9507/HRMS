import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Input from "../../../components/common/Input";
import Button from "../../../components/common/Button";

function LeaveApply() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    leave_type_id: "",
    start_date: "",
    end_date: "",
    reason: "",
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

    if (!form.leave_type_id) {
      setError("Please select a leave type.");
      return;
    }

    if (!form.start_date || !form.end_date) {
      setError("Please select the leave dates.");
      return;
    }

    if (!form.reason.trim()) {
      setError("Please enter a reason.");
      return;
    }

    // API integration in Part 34.

    navigate("/user/leaves");
  }

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Apply Leave</h1>
          <p>
            Submit a new leave request
          </p>
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

        <div className="form-group">
          <label htmlFor="leave_type_id">
            Leave Type
          </label>

          <select
            id="leave_type_id"
            name="leave_type_id"
            value={form.leave_type_id}
            onChange={handleChange}
            required
          >
            <option value="">
              Select Leave Type
            </option>

            <option value="1">
              Casual Leave
            </option>

            <option value="2">
              Sick Leave
            </option>

            <option value="3">
              Earned Leave
            </option>
          </select>
        </div>

        <div className="form-grid">

          <Input
            label="Start Date"
            type="date"
            name="start_date"
            value={form.start_date}
            onChange={handleChange}
            required
          />

          <Input
            label="End Date"
            type="date"
            name="end_date"
            value={form.end_date}
            onChange={handleChange}
            required
          />

        </div>

        <div className="form-group">
          <label htmlFor="reason">
            Reason
          </label>

          <textarea
            id="reason"
            name="reason"
            value={form.reason}
            onChange={handleChange}
            rows="5"
            maxLength="1000"
            required
          />
        </div>

        <div className="form-actions">

          <Button type="submit">
            Submit Leave
          </Button>

          <Button
            type="button"
            className="btn-secondary"
            onClick={() =>
              navigate("/user/leaves")
            }
          >
            Cancel
          </Button>

        </div>

      </form>
    </Layout>
  );
}

export default LeaveApply;