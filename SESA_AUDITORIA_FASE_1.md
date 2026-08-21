# Auditoria funcional inicial do SESA

## Estado atual

O repositório contém a interface SESA em `SESA/index.html`, uma versão alternativa em `SESA-v2/index.html`, backend FastAPI em `backend/app.py`, autenticação em `backend/auth.py` e scripts locais de inicialização. A landing page principal permanece na raiz do repositório.

## Capacidades já presentes

O backend já possui autenticação por sessão, perfis e permissões, CRUD de usuários, configurações editáveis de agentes, propostas de alteração por reunião de RH, configuração editável de orquestração, persistência de conversas em SQLite, registro de auditoria, classificação de assuntos sensíveis, rotas de fontes/Drive e rota principal `/api/chat`.

A interface já possui menu lateral, conversas anteriores, Workflow, configurações Master, identificação do modo de trabalho e eventos de processamento.

## Bloqueios e riscos prioritários

1. A resposta em tempo real depende de `GROQ_API_KEY` no `.env.local`; sem essa variável o backend deve responder de forma controlada ou bloquear a geração.
2. A rota `/api/chat` chama `groq_chat`, portanto é necessário validar configuração, formato da resposta e tratamento de falhas antes de considerar o atendimento real pronto.
3. A rota de mensagens persistidas chama `live_agent_response` com um contexto de usuário que precisa ser validado, pois há caminhos que passam um dicionário e outros que passam apenas o nome do ator.
4. O CrewAI é opcional no import e precisa ser validado no ambiente local antes de ser usado como executor real.
5. O acesso à pasta do Google Drive ainda está representado por `SESA_DRIVE_ROOT` e pastas sincronizadas localmente; não há integração autenticada com a API do Google Drive nesta etapa.
6. A lógica de assuntos sensíveis já diferencia bloqueio de conteúdo e orientação operacional, mas precisa de testes de ponta a ponta por setor, função, permissão e componente documental.

## Primeiro incremento recomendado

Antes de implementar novos agentes, validar o ciclo mínimo: login de usuário padrão, criação/retomada de conversa com o Gestor, envio de mensagem, roteamento, resposta controlada, eventos do Workflow, persistência da mensagem e retorno ao histórico. Em seguida, validar o mesmo ciclo com Master em modo Desenvolvedor e uma reunião com o agente selecionado.

## Arquitetura de execução

Para o estágio atual, manter o backend FastAPI local sincronizado com a pasta de trabalho e a interface publicada no GitHub Pages. A integração autenticada com Google Drive deve ser implementada depois da validação do ciclo local, evitando misturar falhas de credencial externa com falhas de orquestração.
