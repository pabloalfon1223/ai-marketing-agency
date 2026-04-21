import React from 'react';

export const Table: React.FC<React.HTMLAttributes<HTMLTableElement>> = ({
  className = '',
  ...props
}) => (
  <table className={`w-full border-collapse text-sm ${className}`} {...props} />
);

export const TableHeader: React.FC<React.HTMLAttributes<HTMLTableSectionElement>> = ({
  className = '',
  ...props
}) => <thead className={`border-b border-gray-200 ${className}`} {...props} />;

export const TableBody: React.FC<React.HTMLAttributes<HTMLTableSectionElement>> = ({
  className = '',
  ...props
}) => <tbody className={`${className}`} {...props} />;

export const TableRow: React.FC<React.HTMLAttributes<HTMLTableRowElement>> = ({
  className = '',
  ...props
}) => (
  <tr className={`border-b border-gray-200 transition-colors hover:bg-gray-50 ${className}`} {...props} />
);

export const TableHead: React.FC<React.ThHTMLAttributes<HTMLTableCellElement>> = ({
  className = '',
  ...props
}) => (
  <th className={`px-4 py-3 text-left font-semibold text-gray-700 ${className}`} {...props} />
);

export const TableCell: React.FC<React.TdHTMLAttributes<HTMLTableCellElement>> = ({
  className = '',
  ...props
}) => <td className={`px-4 py-3 ${className}`} {...props} />;
