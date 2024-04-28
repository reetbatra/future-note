import React from 'react';

const Button = ({ onClick, className, children }) => {
  // Default button classes
  const defaultClasses = "rounded px-4 py-2 bg-custom-beige hover:bg-custom-light text-black text-bold";

  return (
    <button onClick={onClick} className={`${defaultClasses} ${className}`}>
      {children}
    </button>
  );
};

export default Button;
