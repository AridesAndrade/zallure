# Zallure - Documento de Contexto e Migração

Este documento consolida todas as diretrizes de design, posicionamento estratégico, arquitetura técnica e histórico de decisões do projeto **Zallure**, servindo como base definitiva para retomada ou migração para um novo ambiente de desenvolvimento conectado ao repositório GitHub.

## 1. Visão Geral da Marca e Posicionamento

A **Zallure** opera sob o conceito central de **"The Hotel Experience"**. O objetivo da marca não é o comércio tradicional de cama, mesa e banho, mas sim a tradução da experiência de hospedagem em hotéis cinco estrelas para o ambiente residencial do cliente [1].

| Dimensão Estratégica | Diretriz Aplicada |
| :--- | :--- |
| **Posicionamento** | Experiência hoteleira sofisticada aplicada à residência e a hospedagens de alto padrão. |
| **Tagline Oficial** | `The Hotel Experience | Produtos Premium para Hotelaria` |
| **Tom de Voz** | Sofisticado, acolhedor, editorial e focado em bem-estar e durabilidade. |
| **Restrição de Conteúdo** | Os produtos (enxoval, capas de edredom, mantas, peseiras, saias box e acessórios) não devem ser destacados como "marca própria" ou itens genéricos; o foco é a qualidade e o padrão hoteleiro. |

## 2. Identidade Visual e Especificações de Design

O projeto adota uma estética limpa, alinhada a padrões de hotéis boutique internacionais, evitando ruídos visuais ou elementos excessivamente comerciais.

- **Paleta de Cores Principal:**
  - **Verde Petróleo / Teal Escuro (`#28595A`):** Utilizado em barras de destaque, elementos institucionais e na faixa de rodapé.
  - **Ouro Suave (`#F3C533`):** Empregado em detalhes, taglines e acentos visuais.
  - **Branco Quente e Off-White (`#f5f3f0`):** Fundos e áreas de respiro.
- **Tipografia:**
  - **Títulos:** *Playfair Display* (serifada, elegante).
  - **Corpo de Texto:** *Montserrat* (sem serifa, limpa e legível).
- **Logotipo e Ativos:**
  - O logotipo oficial da Zallure (`logo.png`) está presente no cabeçalho.
  - Os arquivos de imagem da campanha e dos produtos (`luna-lum-quarto.webp`, `luna-lum-capa-edredom.webp`, `luna-lum-saia-box.webp`, `luna-lum-manta-piquet.webp`, `luna-lum-protetor-colchao.webp`, `luna-lum-manta-cashmere.webp`, `luna-lum-peseira.webp`, `luna-lum-enxoval.webp`, `luna-lum-detalhe-cama.webp`, `luna-lum-banho.webp`) compõem a galeria visual do site.

## 3. Arquitetura Técnica e Infraestrutura

O repositório foi estruturado para garantir máxima estabilidade de build e compatibilidade direta com o GitHub Pages [2].

- **Repositório GitHub:** `AridesAndrade/zallure` (Branch principal: `main`) [3].
- **Domínio Personalizado:** `www.zallure.com.br` com suporte a HTTPS e arquivo `CNAME` configurado na raiz [4].
- **Stack Tecnológica:** HTML5 estruturado, CSS avançado com variáveis responsivas, fontes via Google Fonts e imagens otimizadas em WebP [5].
- **Publicação:** O arquivo `index.html` na raiz do repositório atua como artefato principal servido diretamente pelo GitHub Pages, assegurando que o domínio exiba sempre a versão mais recente sem falhas de roteamento de cliente [6].

## 4. Regras de Comportamento e Interação

Para preservar as decisões já validadas pelo usuário, qualquer alteração futura deve respeitar rigorosamente os seguintes pontos:

1. **Botão Principal (CTA):** O botão de destaque no topo ("Explorar Coleção") funciona como uma âncora interna (`#colecao`), levando diretamente o usuário para a seção de apresentação dos produtos.
2. **Links de Destino:** O link da "Loja Amazon" e os demais pontos de contato apontam de forma controlada conforme alinhamento temporário do projeto, preservando a integridade dos textos de rodapé.
3. **E-mail de Contato:** O endereço oficial ativo no rodapé é `zallure1@gmail.com` [7].
4. **Isolamento de Alterações:** Ao receber novas demandas de desenvolvimento ou ajuste visual, nunca modificar o cabeçalho, a tipografia principal ou a estrutura da hero sem consentimento explícito.

---

### Referências
- [1] Documento de Posicionamento Estratégico Zallure (2026).
- [2] Documentação interna do projeto estático Zallure (2026).
- [3] Repositório Oficial GitHub: `https://github.com/AridesAndrade/zallure`.
- [4] Configuração de DNS e CNAME para `www.zallure.com.br`.
- [5] Especificações técnicas do build Vite e HTML estático (2026).
- [6] Diretrizes de implantação contínua em GitHub Pages.
- [7] Diretório de contatos e canais oficiais Zallure.
