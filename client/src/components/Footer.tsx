/**
 * Footer Component - Zallure Landing Page
 * 
 * Design Philosophy:
 * - Clean, minimal footer with brand info
 * - Links to main sections
 * - Copyright and branding
 */

export default function Footer() {
  return (
    <footer className="bg-[#F6F6F2] border-t border-border py-12 md:py-16">
      <div className="container">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Brand Info */}
          <div className="space-y-4">
            <div className="flex flex-col gap-4">
              <img
                src="/manus-storage/LogoZallureretangular_13e7f00b.png"
                alt="Zallure Logo"
                className="h-8 w-auto self-start"
              />
              <img
                src="/luna-lum-new.png"
                alt="Selo Luna LUM"
                className="h-16 w-auto self-start"
              />
            </div>
            <p className="text-sm text-[#556565]">
              Produtos inteligentes que facilitam sua vida.
            </p>
          </div>

          {/* Links */}
          <div className="space-y-3">
            <h4 className="font-semibold text-[#28595A] text-sm">Navegação</h4>
            <ul className="space-y-2 text-sm text-[#556565]">
              <li>
                <a href="#shop" className="hover:text-[#28595A] transition-colors">
                  Shop
                </a>
              </li>
              <li>
                <a href="#about" className="hover:text-[#28595A] transition-colors">
                  Sobre
                </a>
              </li>
              <li>
                <a href="#science" className="hover:text-[#28595A] transition-colors">
                  The Science
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div className="space-y-3">
            <h4 className="font-semibold text-[#28595A] text-sm">Legal</h4>
            <ul className="space-y-2 text-sm text-[#556565]">
              <li>
                <a href="#privacy" className="hover:text-[#28595A] transition-colors">
                  Privacidade
                </a>
              </li>
              <li>
                <a href="#terms" className="hover:text-[#28595A] transition-colors">
                  Termos
                </a>
              </li>
              <li>
                <a href="#contact" className="hover:text-[#28595A] transition-colors">
                  Contato
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-border pt-8">
          <p className="text-center text-sm text-[#556565]">
            © 2026 Zallure. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}
