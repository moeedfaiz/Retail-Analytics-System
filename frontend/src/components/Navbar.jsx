import './Navbar.css';
import { FaSnowflake } from 'react-icons/fa';

function Navbar() {
  return (
    <nav className='navbar'>
      <div className='logo'>
        <FaSnowflake size={30} />
        <div>
          <h2>Retail Analytics</h2>
          <span>Chiller SKU Detection Dashboard</span>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
