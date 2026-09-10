import {
  getAccessToken,
  removeAccessToken,
} from "../utils/storage";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000/api/v1";


export async function apiRequest(
  endpoint,
  options = {}
) {
  const token =
    getAccessToken();

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization =
      `Bearer ${token}`;
  }

  const response =
    await fetch(
      `${API_BASE_URL}${endpoint}`,
      {
        method: "GET",
        ...options,
        headers,
      }
    );


  let data = null;

  const contentType =
    response.headers.get(
      "content-type"
    );

  if (
    contentType &&
    contentType.includes(
      "application/json"
    )
  ) {
    data = await response.json();
  }


  if (!response.ok) {

    if (
      response.status === 401
    ) {
      removeAccessToken();
    }

    const message =
      data?.detail ||
      data?.message ||
      `Request failed with status ${response.status}`;

    throw new Error(message);
  }


  return data;
}


export {
  API_BASE_URL
};


export default apiRequest;