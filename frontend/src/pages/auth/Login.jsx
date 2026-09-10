import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Input from "../../components/common/Input";
import Button from "../../components/common/Button";
import ErrorMessage from "../../components/common/ErrorMessage";

import { login } from "../../services/auth";


function Login() {

  const navigate =
    useNavigate();


  const [form, setForm] =
    useState({
      email: "",
      password: "",
    });


  const [error, setError] =
    useState("");


  const [loading, setLoading] =
    useState(false);


  function handleChange(event) {

    const {
      name,
      value
    } = event.target;


    setForm(
      previous => ({
        ...previous,
        [name]: value,
      })
    );
  }


  async function handleSubmit(
    event
  ) {

    event.preventDefault();

    setError("");
    setLoading(true);


    try {

      const response =
        await login(
          form.email,
          form.password
        );


      if (
        response?.requires_otp
      ) {

        navigate(
          "/verify-otp"
        );

        return;
      }


      setError(
        "OTP verification is required."
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
          HRMS Login
        </h1>


        <p className="auth-subtitle">
          Sign in to your account
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
            label="Email"
            name="email"
            type="email"
            value={
              form.email
            }
            onChange={
              handleChange
            }
            placeholder="Enter your email"
            required
          />


          <Input
            label="Password"
            name="password"
            type="password"
            value={
              form.password
            }
            onChange={
              handleChange
            }
            placeholder="Enter your password"
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
                ? "Signing in..."
                : "Sign In"
            }
          </Button>

        </form>


        <button
          className="link-button"
          onClick={() =>
            navigate(
              "/forgot-password"
            )
          }
        >
          Forgot Password?
        </button>

      </div>

    </div>
  );
}


export default Login;