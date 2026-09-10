import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Input from "../../components/common/Input";
import Button from "../../components/common/Button";
import ErrorMessage from "../../components/common/ErrorMessage";

import { verifyOtp } from "../../services/auth";


function VerifyOtp() {

  const navigate =
    useNavigate();


  const [otp, setOtp] =
    useState("");


  const [error, setError] =
    useState("");


  const [loading, setLoading] =
    useState(false);


  async function handleSubmit(
    event
  ) {

    event.preventDefault();

    setError("");
    setLoading(true);


    try {

      await verifyOtp(
        otp
      );


      navigate(
        "/user/dashboard"
      );

    } catch (err) {

      setError(
        err.message
      );

    } finally {

      setLoading(false);
    }
  }


  return (
    <div className="auth-page">

      <div className="auth-card">

        <h1>
          Verify OTP
        </h1>


        <p className="auth-subtitle">
          Enter the OTP sent to your email.
        </p>


        <ErrorMessage
          message={error}
        />


        <form
          onSubmit={
            handleSubmit
          }
        >

          <Input
            label="OTP"
            name="otp"
            type="text"
            value={otp}
            onChange={
              event =>
                setOtp(
                  event.target.value
                )
            }
            placeholder="Enter 6-digit OTP"
            maxLength={6}
            required
          />


          <Button
            type="submit"
            disabled={
              loading
            }
            className="btn-primary"
          >
            {
              loading
                ? "Verifying..."
                : "Verify OTP"
            }
          </Button>

        </form>

      </div>

    </div>
  );
}


export default VerifyOtp;