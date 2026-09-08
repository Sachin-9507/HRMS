import {
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "../pages/auth/Login";
import VerifyOtp from "../pages/auth/VerifyOtp";
import ForgotPassword from "../pages/auth/ForgotPassword";

import UserDashboard from "../pages/user/UserDashboard";

import AdminDashboard from "../pages/admin/AdminDashboard";

import EmployeeList from "../pages/admin/employees/EmployeeList";
import EmployeeCreate from "../pages/admin/employees/EmployeeCreate";
import EmployeeEdit from "../pages/admin/employees/EmployeeEdit";

import UserList from "../pages/admin/users/UserList";
import UserCreate from "../pages/admin/users/UserCreate";
import UserEdit from "../pages/admin/users/UserEdit";

import RoleList from "../pages/admin/roles/RoleList";
import RoleEdit from "../pages/admin/roles/RoleEdit";

import PermissionList from "../pages/admin/permissions/PermissionList";

import AttendanceList from "../pages/admin/attendance/AttendanceList";
import AttendanceEdit from "../pages/admin/attendance/AttendanceEdit";

import LeaveList from "../pages/admin/leaves/LeaveList";
import LeaveReview from "../pages/admin/leaves/LeaveReview";

import AuditLogList from "../pages/admin/audit/AuditLogList";

import NotFound from "../pages/NotFound";


import Profile from "../pages/user/Profile";

import AttendanceToday
  from "../pages/user/attendance/AttendanceToday";

import AttendanceHistory
  from "../pages/user/attendance/AttendanceHistory";

import LeaveBalance
  from "../pages/user/leaves/LeaveBalance";

import LeaveApply
  from "../pages/user/leaves/LeaveApply";


import LeaveDetails
  from "../pages/user/leaves/LeaveDetails";


function AppRoutes() {
  return (
    <Routes>
      {/* Authentication */}
      <Route
        path="/"
        element={<Navigate to="/login" replace />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/verify-otp"
        element={<VerifyOtp />}
      />

      <Route
        path="/forgot-password"
        element={<ForgotPassword />}
      />

      {/* User */}
      <Route
        path="/user/dashboard"
        element={<UserDashboard />}
      />

      {/* Admin */}
      <Route
        path="/admin/dashboard"
        element={<AdminDashboard />}
      />

      {/* Employees */}
      <Route
        path="/admin/employees"
        element={<EmployeeList />}
      />

      <Route
        path="/admin/employees/create"
        element={<EmployeeCreate />}
      />

      <Route
        path="/admin/employees/:employeeId/edit"
        element={<EmployeeEdit />}
      />

      {/* Users */}
      <Route
        path="/admin/users"
        element={<UserList />}
      />

      <Route
        path="/admin/users/create"
        element={<UserCreate />}
      />

      <Route
        path="/admin/users/:userId/edit"
        element={<UserEdit />}
      />

      {/* Roles */}
      <Route
        path="/admin/roles"
        element={<RoleList />}
      />

      <Route
        path="/admin/roles/:roleId/edit"
        element={<RoleEdit />}
      />

      {/* Permissions */}
      <Route
        path="/admin/permissions"
        element={<PermissionList />}
      />

      {/* Attendance */}
      <Route
        path="/admin/attendance"
        element={<AttendanceList />}
      />

      <Route
        path="/admin/attendance/:attendanceId/edit"
        element={<AttendanceEdit />}
      />

      {/* Leaves */}
      <Route
        path="/admin/leaves"
        element={<LeaveList />}
      />

      <Route
        path="/admin/leaves/:leaveId"
        element={<LeaveReview />}
      />

      {/* Audit */}
      <Route
        path="/admin/audit-logs"
        element={<AuditLogList />}
      />

      {/* 404 */}
      <Route
        path="*"
        element={<NotFound />}

      />
      <Route
  path="/user/dashboard"
  element={<UserDashboard />}
/>

<Route
  path="/user/profile"
  element={<Profile />}
/>

<Route
  path="/user/attendance/today"
  element={<AttendanceToday />}
/>

<Route
  path="/user/attendance/history"
  element={<AttendanceHistory />}
/>

<Route
  path="/user/leaves/balance"
  element={<LeaveBalance />}
/>

<Route
  path="/user/leaves"
  element={<LeaveList />}
/>

<Route
  path="/user/leaves/apply"
  element={<LeaveApply />}
/>

<Route
  path="/user/leaves/:leaveId"
  element={<LeaveDetails />}
/>
    </Routes>
  );
}

export default AppRoutes;

