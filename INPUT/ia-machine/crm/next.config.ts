import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Todas las rutas son dinámicas — el CRM requiere auth y acceso a DB en runtime
  experimental: {},
};

export default nextConfig;
