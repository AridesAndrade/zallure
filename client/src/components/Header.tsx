/**
 * Header Component - Zallure Landing Page
 * 
 * Design Philosophy:
 * - Clean, minimalist navigation with generous spacing
 * - Logo (left) + Menu (center) + Icons (right)
 * - Verde Petróleo (#28595A) for logo and accents
 * - Subtle hover effects, no heavy shadows
 */

import { Search, User } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white border-b border-border">
      <div className="container flex items-center justify-between py-4">
        {/* Logo */}
        <div className="flex items-center">
          <img
            src="/manus-storage/LogoZallureretangular_13e7f00b.png"
            alt="Zallure Logo"
            className="h-10 w-auto"
          />
        </div>

        {/* Menu Principal */}
        <nav className="hidden md:flex items-center gap-8">
          <a
            href="#shop"
            className="text-sm font-medium text-foreground hover:text-[#28595A] transition-colors"
          >
            Shop
          </a>
          <a
            href="#about"
            className="text-sm font-medium text-foreground hover:text-[#28595A] transition-colors"
          >
            About
          </a>
          <a
            href="#science"
            className="text-sm font-medium text-foreground hover:text-[#28595A] transition-colors"
          >
            The Science
          </a>
          <a
            href="#customers"
            className="text-sm font-medium text-foreground hover:text-[#28595A] transition-colors"
          >
            Happy Customers
          </a>
        </nav>

        {/* Ícones Direita */}
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            className="text-foreground hover:text-[#28595A]"
          >
            <Search className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="text-foreground hover:text-[#28595A]"
          >
            <User className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
}
