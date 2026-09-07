import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Input from "../../components/common/Input";
import Button from "../../components/common/Button";
import ErrorMessage from "../../components/common/ErrorMessage";
import apiRequest from "../../services/api";

function VerifyOtp() {
  const navigate = useNavigate();

  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await apiRequest("/auth/verify-otp", {
        method: "POST",
        body: JSON.stringify({
          otp,
        }),
      });

      

      navigate("/user/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Verify OTP</h1>

        <p className="auth-subtitle">
          Enter the OTP sent to your email.
        </p>

        <ErrorMessage message={error} />

        <form onSubmit={handleSubmit}>
          <Input
            label="OTP"
            name="otp"
            type="text"
            value={otp}
            onChange={(event) => setOtp(event.target.value)}
            placeholder="Enter OTP"
            required
          />

          <Button
            type="submit"
            disabled={loading}
            className="btn-primary"
          >
            {loading ? "Verifying..." : "Verify OTP"}
          </Button>
        </form>
      </div>
    </div>
  );
}

export default VerifyOtp;