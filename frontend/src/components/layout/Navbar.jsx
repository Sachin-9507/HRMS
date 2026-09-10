import { useNavigate } from "react-router-dom";

import { APP_NAME } from "../../utils/constants";
import { logout } from "../../services/auth";


function Navbar() {

  const navigate =
    useNavigate();


  function handleLogout() {

    logout();

    navigate(
      "/login",
      { replace: true }
    );
  }


  return (

    <header className="navbar">

      <div className="navbar-brand">
        {APP_NAME}
      </div>


      <div className="navbar-user">

        <span>
          Welcome
        </span>


        <button
          type="button"
          className="btn btn-secondary"
          onClick={
            handleLogout
          }
        >
          Logout
        </button>

      </div>

    </header>
  );
}


export default Navbar;