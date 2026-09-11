import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import {
  getAccessToken,
  removeAccessToken,
} from "../utils/storage";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(
    getAccessToken()
  );

  const [user, setUser] = useState(null);

  const isAuthenticated = Boolean(token);

  function updateToken(newToken) {
    setToken(newToken);
  }

  function updateUser(userData) {
    setUser(userData);
  }

  function logout() {
    removeAccessToken();
    setToken(null);
    setUser(null);
  }

  useEffect(() => {
    function handleStorageChange() {
      setToken(getAccessToken());
    }

    window.addEventListener(
      "storage",
      handleStorageChange
    );

    return () => {
      window.removeEventListener(
        "storage",
        handleStorageChange
      );
    };
  }, []);

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

export function useAuth() {
  return useContext(AuthContext);
}