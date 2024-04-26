import React from 'react';

const Button = ({ onClick, className, children }) => {
  // Default button classes
  const defaultClasses = "rounded px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white";

  return (
    <button onClick={onClick} className={`${defaultClasses} ${className}`}>
      {children}
    </button>
  );
};

export default Button;
