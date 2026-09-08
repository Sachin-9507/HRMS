import { useParams, useNavigate } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Button from "../../../components/common/Button";
import Badge from "../../../components/common/Badge";

function LeaveDetails() {
  const { leaveId } = useParams();
  const navigate = useNavigate();

  const leave = null;

  function handleCancel() {
    // API integration in Part 34.
  }

  return (
    <Layout>
      <div className="leave-details-page">

        <div className="leave-details-header">
          <div>
            <h1>Leave Details</h1>

            <p>
              Leave Request #{leaveId}
            </p>
          </div>
        </div>


        <div className="leave-details-card">

          <div className="leave-detail-row">
            <span className="leave-detail-label">
              Leave Type
            </span>

            <strong className="leave-detail-value">
              {leave?.leave_type_name || "-"}
            </strong>
          </div>


          <div className="leave-detail-row">
            <span className="leave-detail-label">
              Start Date
            </span>

            <strong className="leave-detail-value">
              {leave?.start_date || "-"}
            </strong>
          </div>


          <div className="leave-detail-row">
            <span className="leave-detail-label">
              End Date
            </span>

            <strong className="leave-detail-value">
              {leave?.end_date || "-"}
            </strong>
          </div>


          <div className="leave-detail-row">
            <span className="leave-detail-label">
              Total Days
            </span>

            <strong className="leave-detail-value">
              {leave?.total_days || "-"}
            </strong>
          </div>


          <div className="leave-detail-row">
            <span className="leave-detail-label">
              Status
            </span>

            <div className="leave-detail-value">
              <Badge
                status={leave?.status || "PENDING"}
              />
            </div>
          </div>


          <div className="leave-detail-row leave-reason-row">
            <span className="leave-detail-label">
              Reason
            </span>

            <strong className="leave-detail-value">
              {leave?.reason || "-"}
            </strong>
          </div>


          <div className="leave-detail-row leave-remarks-row">
            <span className="leave-detail-label">
              Admin Remarks
            </span>

            <strong className="leave-detail-value">
              {leave?.admin_remarks || "-"}
            </strong>
          </div>


          <div className="leave-details-actions">

            {leave?.status === "PENDING" && (
              <Button
                type="button"
                className="btn-danger"
                onClick={handleCancel}
              >
                Cancel Leave
              </Button>
            )}

            <Button
              type="button"
              className="btn-secondary"
              onClick={() => navigate("/user/leaves")}
            >
              Back
            </Button>

          </div>

        </div>
      </div>
    </Layout>
  );
}

export default LeaveDetails;