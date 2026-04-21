import React, { useState } from 'react';

interface SelectContextType {
  value: string;
  onValueChange: (value: string) => void;
}

const SelectContext = React.createContext<SelectContextType | undefined>(undefined);

interface SelectProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: string;
  onValueChange?: (value: string) => void;
}

export const Select: React.FC<SelectProps> = ({ value = '', onValueChange, children }) => {
  const [internalValue, setInternalValue] = useState(value);
  const currentValue = value !== undefined ? value : internalValue;

  const handleValueChange = (newValue: string) => {
    setInternalValue(newValue);
    onValueChange?.(newValue);
  };

  return (
    <SelectContext.Provider value={{ value: currentValue, onValueChange: handleValueChange }}>
      <div>{children}</div>
    </SelectContext.Provider>
  );
};

export const SelectTrigger: React.FC<React.HTMLAttributes<HTMLButtonElement>> = ({
  className = '',
  ...props
}) => (
  <button
    className={`flex h-10 w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none ${className}`}
    {...props}
  />
);

export const SelectValue: React.FC<{ placeholder?: string }> = ({ placeholder = 'Select...' }) => {
  const context = React.useContext(SelectContext);
  return <span>{context?.value || placeholder}</span>;
};

export const SelectContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className = '',
  ...props
}) => (
  <div
    className={`absolute top-full left-0 right-0 mt-1 rounded-md border border-gray-300 bg-white shadow-lg z-50 ${className}`}
    {...props}
  />
);

export const SelectItem: React.FC<
  React.HTMLAttributes<HTMLDivElement> & { value: string }
> = ({ className = '', value, children, ...props }) => {
  const context = React.useContext(SelectContext);

  return (
    <div
      className={`px-3 py-2 cursor-pointer hover:bg-gray-100 ${
        context?.value === value ? 'bg-blue-50 text-blue-900' : ''
      } ${className}`}
      onClick={() => context?.onValueChange(value)}
      {...props}
    >
      {children}
    </div>
  );
};
