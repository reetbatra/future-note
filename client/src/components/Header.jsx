import React from 'react';
import logo from '../assets/logo.png'; 

const Header = () => {
  return (
    <div className="h-20 flex justify-between items-center px-4 py-2 bg-custom-blue text-white"> 
      <div className="flex items-center">
        <img src={logo} alt="Logo" className="h-8 mr-2" /> 
      </div>
      <div>
        <button className="mr-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">Sign In</button>
        <button className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded">Sign Up</button>
      </div>
    </div>
  );
};

export default Header;


