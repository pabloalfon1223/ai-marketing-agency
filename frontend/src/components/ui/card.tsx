import React from 'react';

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className = '',
  ...props
}) => (
  <div className={`rounded-lg border border-gray-200 bg-white shadow-sm ${className}`} {...props} />
);

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className = '',
  ...props
}) => <div className={`px-6 py-4 ${className}`} {...props} />;

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({
  className = '',
  ...props
}) => <h3 className={`text-lg font-semibold ${className}`} {...props} />;

export const CardDescription: React.FC<React.HTMLAttributes<HTMLParagraphElement>> = ({
  className = '',
  ...props
}) => <p className={`text-sm text-gray-600 ${className}`} {...props} />;

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className = '',
  ...props
}) => <div className={`px-6 py-4 ${className}`} {...props} />;
