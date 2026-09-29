import {
  useEffect,
  useState,
} from "react";

import AuthContext from "./AuthContext";

import {
  getAccessToken,
  removeAccessToken,
} from "../utils/storage";

export default function AuthProvider({ children }) {
  const [token, setToken] = useState(getAccessToken());
  const [user, setUser] = useState(null);

  const isAuthenticated = Boolean(token);

  useEffect(() => {
    // Existing logic
  }, [token]);

  const updateToken = (newToken) => {
    setToken(newToken);
  };

  const updateUser = (newUser) => {
    setUser(newUser);
  };

  const logout = () => {
    removeAccessToken();
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        isAuthenticated,
        updateToken,
        updateUser,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}