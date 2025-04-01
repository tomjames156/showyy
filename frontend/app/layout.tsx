import type { Metadata } from "next";
import { inter } from '@/app/ui/fonts'

export const metadata: Metadata = {
  title: "Tomi's Portfolio",
  description: "Portfolio Website by Akinwande Tomisin",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <link rel="icon" type="/icon.png" href="/favicon-new.png" sizes="32x32"/>
      <link
        rel="apple-touch-icon"
        type="image/png" href="/icon.png" sizes="32x32"
      />
      <body
        className={`${inter.className} antialiased dark:bg-black dark:text`}
      >
        {children}
      </body>
    </html>
  );
}
