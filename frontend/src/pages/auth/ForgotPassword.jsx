import { useState } from "react";

import Input from "../../components/common/Input";
import Button from "../../components/common/Button";
import ErrorMessage from "../../components/common/ErrorMessage";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    setMessage("");
    setError("");

    

    if (!email) {
      setError("Email is required.");
      return;
    }

    setMessage(
      "Password reset functionality will be connected to the backend."
    );
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Forgot Password</h1>

        <p className="auth-subtitle">
          Enter your registered email address.
        </p>

        <ErrorMessage message={error} />

        {message && (
          <div className="success-message">
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <Input
            label="Email"
            name="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="Enter your email"
            required
          />

          <Button
            type="submit"
            className="btn-primary"
          >
            Send Reset Request
          </Button>
        </form>
      </div>
    </div>
  );
}

export default ForgotPassword;