import React from 'react';
import Button from './Button'; 
import logo from '../assets/logo.png';

const Header = () => {
  return (
    <div className="h-20 flex justify-between items-center px-4 py-2 bg-custom-blue text-white">
      <div className="flex items-center">
        <img src={logo} alt="Logo" className="h-8 mr-2" />
      </div>
      <div>
        {/* Use the Button component */}
        <Button className="mr-4">Sign In</Button>
        <Button className="bg-green-500 hover:bg-green-600">Sign Up</Button>
      </div>
    </div>
  );
};

export default Header;


