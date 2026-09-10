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


const AuthContext =
  createContext(null);


export function AuthProvider({
  children,
}) {

  const [token, setToken] =
    useState(
      getAccessToken()
    );


  const isAuthenticated =
    Boolean(token);


  function updateToken(
    newToken
  ) {
    setToken(newToken);
  }


  function logout() {

    removeAccessToken();

    setToken(null);
  }


  useEffect(() => {

    function handleStorageChange() {

      setToken(
        getAccessToken()
      );
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
        isAuthenticated,
        updateToken,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {

  return useContext(
    AuthContext
  );
}