import apiRequest from "./api";

import {
  setAccessToken,
  setLoginUserId,
  removeAccessToken,
  removeLoginUserId,
} from "../utils/storage";


export async function login(
  email,
  password
) {
  const params = new URLSearchParams({
    email,
    password,
  });

  const response = await apiRequest(
    `/Auth/login?${params.toString()}`,
    {
      method: "POST",
    }
  );

  if (response?.user_id) {
    setLoginUserId(
      response.user_id
    );
  }

  return response;
}


export async function verifyOtp(
  otp
) {
  const userId =
    localStorage.getItem(
      "hrms_login_user_id"
    );

  if (!userId) {
    throw new Error(
      "Login session not found. Please login again."
    );
  }

  const params = new URLSearchParams({
    user_id: userId,
    otp: otp,
  });

  const response =
    await apiRequest(
      `/Auth/verify-otp?${params.toString()}`,
      {
        method: "POST",
      }
    );

  if (!response?.access_token) {
    throw new Error(
      "Access token was not returned by the server."
    );
  }

  setAccessToken(
    response.access_token
  );

  removeLoginUserId();

  return response;
}


export function logout() {
  removeAccessToken();
  removeLoginUserId();
}