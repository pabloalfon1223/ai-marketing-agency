import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ruido Mental Cero — Mente Pausada",
  description: "El sistema simple para personas con la mente que no para. Ebook + audios guiados en español.",
  openGraph: {
    title: "Ruido Mental Cero",
    description: "El sistema simple para personas con la mente que no para.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
