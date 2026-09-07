import { useParams } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Button from "../../../components/common/Button";

function LeaveReview() {
  const { leaveId } = useParams();

  function handleApprove() {
    // API integration in Part 34.
  }

  function handleReject() {
    // API integration in Part 34.
  }

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Review Leave Request</h1>
          <p>Leave ID: {leaveId}</p>
        </div>
      </div>

      <div className="form-card">
        <p>
          Leave request details will be loaded from the
          backend in Part 34.
        </p>

        <div className="form-actions">
          <Button
            type="button"
            onClick={handleApprove}
          >
            Approve
          </Button>

          <Button
            type="button"
            className="btn-danger"
            onClick={handleReject}
          >
            Reject
          </Button>
        </div>
      </div>
    </Layout>
  );
}

export default LeaveReview;