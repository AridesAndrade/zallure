/**
 * FloatingWidgets Component - Zallure Landing Page
 * 
 * Design Philosophy:
 * - Cupom (esquerda inferior): Verde petróleo com texto branco
 * - Chat (direita inferior): Verde petróleo com ícone branco + badge de notificação
 * - Animação: Fade-in suave, sem movimento excessivo
 */

import { MessageCircle } from "lucide-react";
import { useState } from "react";

export default function FloatingWidgets() {
  const [showChat, setShowChat] = useState(false);

  return (
    <>
      {/* Cupom - Esquerda Inferior */}
      <button
        className="fixed bottom-6 left-6 z-40 bg-[#28595A] text-white px-4 py-3 rounded-full font-semibold text-sm hover:bg-[#1f4345] transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 animate-fade-in" style={{animationDelay: '0.5s'}}
        onClick={() => alert("Cupom: ZALLURE15 - 15% de desconto!")}
      >
        Ganhe 15% OFF
      </button>

      {/* Chat - Direita Inferior */}
      <button
        className="fixed bottom-6 right-6 z-40 bg-[#28595A] text-white w-14 h-14 rounded-full flex items-center justify-center hover:bg-[#1f4345] transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 animate-fade-in" style={{animationDelay: '0.6s'}}
        onClick={() => setShowChat(!showChat)}
      >
        <MessageCircle className="h-6 w-6" />
        {/* Badge de Notificação */}
        <span className="absolute top-0 right-0 w-3 h-3 bg-[#FF3B30] rounded-full animate-pulse" />
      </button>

      {/* Chat Modal */}
      {showChat && (
        <div className="fixed bottom-24 right-6 z-40 bg-white rounded-lg shadow-2xl w-80 max-w-sm">
          <div className="bg-[#28595A] text-white p-4 rounded-t-lg">
            <h3 className="font-semibold">Olá! Como posso ajudar?</h3>
          </div>
          <div className="p-4 space-y-3">
            <p className="text-sm text-[#556565]">
              Estamos aqui para responder suas dúvidas sobre nossos produtos.
            </p>
            <button className="w-full bg-[#F3C533] text-[#111111] py-2 rounded font-semibold text-sm hover:bg-[#E0B82A] transition-colors">
              Iniciar Conversa
            </button>
          </div>
        </div>
      )}
    </>
  );
}
