/**
 * Home Page - Zallure Landing Page
 * 
 * Main landing page with:
 * - Announcement Bar
 * - Header with navigation
 * - Hero section with split layout
 * - Floating widgets (coupon + chat)
 * - Footer
 */

import AnnouncementBar from "@/components/AnnouncementBar";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import FloatingWidgets from "@/components/FloatingWidgets";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <AnnouncementBar />
      <Header />
      <main className="flex-1">
        <Hero />
      </main>
      <Footer />
      <FloatingWidgets />
    </div>
  );
}
