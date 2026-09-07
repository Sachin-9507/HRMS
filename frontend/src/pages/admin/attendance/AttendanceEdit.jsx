import { useParams } from "react-router-dom";

import Layout from "../../../components/layout/Layout";

function AttendanceEdit() {
  const { attendanceId } = useParams();

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Edit Attendance</h1>
          <p>
            Attendance ID: {attendanceId}
          </p>
        </div>
      </div>

      <div className="form-card">
        Attendance editing will be connected to the
        backend in Part 34.
      </div>
    </Layout>
  );
}

export default AttendanceEdit;