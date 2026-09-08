import Layout from "../../../components/layout/Layout";
import Button from "../../../components/common/Button";
import Badge from "../../../components/common/Badge";

function AttendanceToday() {
  const attendance = null;

  function handleCheckIn() {
    // API integration in Part 34.
  }

  function handleCheckOut() {
    // API integration in Part 34.
  }

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Today's Attendance</h1>
          <p>
            Manage your attendance for today
          </p>
        </div>
      </div>

      <div className="attendance-card">

        <div className="attendance-status">
          <span>Status</span>

          <Badge
            status={
              attendance?.status || "NOT CHECKED"
            }
          />
        </div>

        <div className="attendance-info">

          <div>
            <span>Check In</span>
            <strong>
              {attendance?.check_in || "-"}
            </strong>
          </div>

          <div>
            <span>Check Out</span>
            <strong>
              {attendance?.check_out || "-"}
            </strong>
          </div>

          <div>
            <span>Working Minutes</span>
            <strong>
              {attendance?.working_minutes ?? 0}
            </strong>
          </div>

        </div>

        <div className="form-actions">

          <Button
            type="button"
            onClick={handleCheckIn}
          >
            Check In
          </Button>

          <Button
            type="button"
            className="btn-danger"
            onClick={handleCheckOut}
          >
            Check Out
          </Button>

        </div>

      </div>
    </Layout>
  );
}

export default AttendanceToday;