const ACCESS_TOKEN_KEY = "hrms_access_token";
const USER_ID_KEY = "hrms_login_user_id";

export function setAccessToken(token) {
  localStorage.setItem(
    ACCESS_TOKEN_KEY,
    token
  );
}

export function getAccessToken() {
  return localStorage.getItem(
    ACCESS_TOKEN_KEY
  );
}

export function removeAccessToken() {
  localStorage.removeItem(
    ACCESS_TOKEN_KEY
  );
}

export function setLoginUserId(userId) {
  localStorage.setItem(
    USER_ID_KEY,
    String(userId)
  );
}

export function getLoginUserId() {
  const userId =
    localStorage.getItem(USER_ID_KEY);

  return userId
    ? Number(userId)
    : null;
}

export function removeLoginUserId() {
  localStorage.removeItem(
    USER_ID_KEY
  );
}