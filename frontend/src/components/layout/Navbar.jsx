import { APP_NAME } from "../../utils/constants";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-brand">
        {APP_NAME}
      </div>

      <div className="navbar-user">
        <span>Welcome</span>
      </div>
    </header>
  );
}

export default Navbar;