import Layout from "../../components/layout/Layout";

function Profile() {
  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>My Profile</h1>
          <p>
            View your employee information
          </p>
        </div>
      </div>

      <div className="profile-card">

        <div className="profile-row">
          <span>Employee Code</span>
          <strong>-</strong>
        </div>

        <div className="profile-row">
          <span>First Name</span>
          <strong>-</strong>
        </div>

        <div className="profile-row">
          <span>Last Name</span>
          <strong>-</strong>
        </div>

        <div className="profile-row">
          <span>Email</span>
          <strong>-</strong>
        </div>

        <div className="profile-row">
          <span>Phone</span>
          <strong>-</strong>
        </div>

        <div className="profile-row">
          <span>Department</span>
          <strong>-</strong>
        </div>

        <div className="profile-row">
          <span>Designation</span>
          <strong>-</strong>
        </div>

        <div className="profile-row">
          <span>Joining Date</span>
          <strong>-</strong>
        </div>

      </div>
    </Layout>
  );
}

export default Profile;