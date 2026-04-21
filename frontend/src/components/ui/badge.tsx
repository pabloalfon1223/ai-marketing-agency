import React from 'react';

export const Badge: React.FC<React.HTMLAttributes<HTMLSpanElement>> = ({
  className = '',
  ...props
}) => (
  <span
    className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-medium ${className}`}
    {...props}
  />
);
