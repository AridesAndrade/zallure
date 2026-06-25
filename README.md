# Zallure - Landing Page Profissional

Landing page moderna e profissional para a Zallure, com foco em conversão para a loja Amazon.

## 🎨 Design

- **Design Minimalista Premium** inspirado em Grounding Essentials
- **Paleta de Cores**: Verde Petróleo (#28595A) + Ouro (#F3C533)
- **Tipografia**: Montserrat (headlines) + Inter (body)
- **Totalmente Responsivo** (mobile, tablet, desktop)
- **Animações Suaves** com fade-in e hover effects

## ✨ Recursos

- ✅ Barra de anúncios com mensagem de promoção
- ✅ Header com navegação e ícones
- ✅ Hero section com split layout (card + imagem)
- ✅ Benefícios com checkmarks
- ✅ CTA principal em ouro com link direto para Amazon
- ✅ Widgets flutuantes (cupom de desconto + chat)
- ✅ Footer com links e informações
- ✅ Logo oficial Zallure integrada

## 🚀 Tecnologias

- **React 19** - Framework UI
- **Tailwind CSS 4** - Utility-first CSS
- **Vite** - Build tool rápido
- **TypeScript** - Type safety
- **shadcn/ui** - Componentes acessíveis

## 📦 Como Instalar e Rodar Localmente

### Pré-requisitos
- Node.js 18+ instalado
- npm ou pnpm

### Instalação

```bash
# Clone o repositório
git clone https://github.com/AridesAndrade/zallure.git
cd zallure

# Instale as dependências
npm install
# ou
pnpm install
```

### Rodando em Desenvolvimento

```bash
# Inicie o servidor de desenvolvimento
npm run dev
# ou
pnpm dev

# Acesse http://localhost:5173
```

### Build para Produção

```bash
# Crie a build de produção
npm run build
# ou
pnpm build

# Visualize a build
npm run preview
# ou
pnpm preview
```

## 🔗 Links Importantes

- **Loja Amazon**: https://www.amazon.com.br/s?me=A1A4OKNWC2CQ6O&marketplaceID=A2Q3Y263D00KWC
- **Site ao Vivo**: https://www.zallure.com.br
- **GitHub**: https://github.com/AridesAndrade/zallure

## 📁 Estrutura do Projeto

```
zallure/
├── client/
│   ├── public/
│   │   ├── favicon.ico
│   │   └── __manus__/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── AnnouncementBar.tsx
│   │   │   ├── Hero.tsx
│   │   │   ├── FloatingWidgets.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── ui/              # shadcn/ui components
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   └── NotFound.tsx
│   │   ├── contexts/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css             # Tailwind + custom styles
│   └── index.html
├── server/                        # Backend placeholder
├── shared/                        # Shared types
├── package.json
├── vite.config.ts
├── tsconfig.json
├── CNAME                          # Domínio customizado
└── README.md
```

## 🎯 Próximos Passos

1. **Conectar Analytics**: Integre Google Analytics para rastrear cliques
2. **Adicionar Seção de Produtos**: Crie uma grid com produtos em destaque
3. **Newsletter**: Implemente formulário de email marketing
4. **Depoimentos**: Adicione seção com avaliações de clientes reais
5. **SEO**: Otimize meta tags e schema.org

## 🔧 Customização

### Alterar Cores

Edite `client/src/index.css` e procure por:
```css
--color-teal-primary: #28595A;      /* Verde Petróleo */
--color-gold-secondary: #F3C533;    /* Ouro */
```

### Alterar Tipografia

Edite `client/index.html` e procure por:
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
```

### Alterar Link Amazon

Edite `client/src/components/Hero.tsx` e procure por:
```tsx
href="https://www.amazon.com.br/s?me=A1A4OKNWC2CQ6O&marketplaceID=A2Q3Y263D00KWC"
```

## 📝 Licença

© 2026 Zallure. Todos os direitos reservados.

## 👤 Autor

Desenvolvido com ❤️ para Zallure

---

**Dúvidas?** Abra uma issue no repositório ou entre em contato!
