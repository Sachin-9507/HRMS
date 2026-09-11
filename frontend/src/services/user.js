import apiRequest from "./api";

export async function getCurrentUser() {
  return apiRequest("/me");
}