import {
  Navigate,
  Outlet,
} from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function RoleRoute({
  allowedRoles,
}) {
  const {
    isAuthenticated,
    user,
  } = useAuth();

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }

  if (!user) {
    return <Outlet />;
  }

  if (
    !allowedRoles.includes(
      user.role_name
    )
  ) {
    return (
      <Navigate
        to="/user/dashboard"
        replace
      />
    );
  }

  return <Outlet />;
}

export default RoleRoute;