import { Star, Check } from "lucide-react";

const benefits = [
  "Produtos de qualidade comprovada",
  "Seleção rigorosa de inovações",
  "Praticidade para seu dia a dia",
  "Suporte e garantia confiáveis",
];

export default function Hero() {
  return (
    <section className="relative bg-white py-12 md:py-20">
      <div className="container">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 items-center">
          {/* Card Informativo */}
          <div className="bg-[#F6F6F2] rounded-lg p-8 md:p-10 space-y-6 order-2 md:order-1 shadow-sm hover:shadow-md transition-shadow duration-300">
            {/* Headline */}
            <div className="space-y-2">
              <h1 className="text-4xl md:text-5xl font-montserrat font-bold text-[#28595A] leading-tight">
                O Toque dos Melhores Hotéis na Sua Cama
              </h1>
              <p className="text-xl font-medium text-[#28595A]">
                Qualidade e durabilidade hoteleira para o seu dia a dia
              </p>
            </div>

            {/* Rating */}
            <div className="flex items-center gap-2">
              <div className="flex gap-1">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className="h-4 w-4 fill-[#28595A] text-[#28595A]"
                  />
                ))}
              </div>
              <span className="text-sm font-medium text-[#28595A]">
                4.9/5.0 | Baseado em 180+ avaliações
              </span>
            </div>

            {/* Descrição */}
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-[#28595A]">Coleção Hotel Home Zallure</h2>
              <p className="text-base text-[#556565] leading-relaxed">
                Leve para o seu quarto o segredo das melhores estadias. Nossa linha de enxoval premium combina o toque acetinado e o frescor das camas de hotel com a alta durabilidade exigida pelo mercado profissional. Perfeito para sua casa, essencial para sua pousada.
              </p>
            </div>

            {/* Benefits */}
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <Check className="h-5 w-5 text-[#28595A] flex-shrink-0 mt-0.5" />
                <span className="text-sm text-[#556565]">O padrão dos melhores hotéis e Airbnbs, desenhado para resistir a lavagens constantes mantendo o toque macio.</span>
              </li>
              <li className="flex items-start gap-3">
                <Check className="h-5 w-5 text-[#28595A] flex-shrink-0 mt-0.5" />
                <span className="text-sm text-[#556565]">Eleva a estética do seu quarto e transforma o seu momento de descanso em uma experiência 5 estrelas.</span>
              </li>
            </ul>

            {/* CTA Principal */}
            <a
              href="https://www.amazon.com.br/s?me=A1A4OKNWC2CQ6O&marketplaceID=A2Q3Y263D00KWC"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-[#F3C533] text-[#111111] hover:bg-[#E0B82A] font-semibold text-base h-12 px-8 transition-all duration-200 active:scale-95 btn-hover-scale rounded"
            >
              Explorar Produtos
            </a>
          </div>

          {/* Imagem Hero */}
          <div className="relative overflow-hidden rounded-lg order-1 md:order-2">
            <img
              src="https://d2xsxph8kpxj0f.cloudfront.net/310419663029245873/g46GJbRyKveU3WvBqFiKUu/zallure-hero-image-HYMxKdNuC7SY8KgBqW66w7.webp"
              alt="Mulher dormindo em lençol confortável"
              className="w-full h-auto object-cover rounded-lg shadow-lg"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
