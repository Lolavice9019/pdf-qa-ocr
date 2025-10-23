# 📖 Guia do Usuário - Sistema de Perguntas e Respostas com PDF

Bem-vindo ao sistema de Question Answering para documentos PDF! Este guia irá ajudá-lo a aproveitar ao máximo todas as funcionalidades da aplicação.

## 🎯 O que é este sistema?

Este sistema permite que você:
1. **Faça upload de documentos PDF** (mesmo que sejam digitalizados ou imagens)
2. **Extraia automaticamente o texto** usando tecnologia de OCR (Reconhecimento Óptico de Caracteres)
3. **Faça perguntas sobre o conteúdo** e receba respostas inteligentes baseadas no texto extraído

## 🚀 Como começar

### Passo 1: Acesse a aplicação

Abra seu navegador e acesse a URL da aplicação (fornecida pelo administrador ou disponível localmente em `http://localhost:8501`).

### Passo 2: Upload de documentos

1. Na seção **"1. Upload de Documentos PDF"**, clique no botão **"Browse files"**
2. Selecione um ou mais arquivos PDF do seu computador
3. Você pode selecionar múltiplos arquivos de uma vez (Ctrl+Click ou Cmd+Click)

**Limites:**
- Tamanho máximo por arquivo: **1 GB**
- Formatos aceitos: **PDF**
- Número de arquivos: **Ilimitado**

### Passo 3: Aguarde o processamento

O sistema irá:
1. Converter cada página do PDF em imagem
2. Aplicar OCR para extrair o texto
3. Salvar os resultados automaticamente

**Tempo de processamento:**
- Documentos pequenos (< 10 páginas): 1-2 minutos
- Documentos médios (10-50 páginas): 5-10 minutos
- Documentos grandes (> 50 páginas): 10+ minutos

**Barra de progresso:**
- Acompanhe o processamento em tempo real
- Veja quantas páginas já foram processadas

### Passo 4: Visualize os documentos processados

Na seção **"2. Documentos Processados"**:

1. **Expanda o documento** clicando no nome do arquivo
2. **Veja informações gerais:**
   - Número de páginas
   - Caminho do log de OCR
   - Total de caracteres extraídos

3. **Visualize o texto por página:**
   - Clique em "Página X" para ver o texto extraído
   - Compare com o PDF original para verificar a precisão
   - Use para validar a qualidade do OCR

### Passo 5: Faça perguntas

Na seção **"3. Fazer Perguntas"**:

1. **Selecione o documento** no menu dropdown
2. **Digite sua pergunta** no campo de texto
3. **Clique em "🔍 Buscar Resposta"**
4. **Aguarde o processamento** (geralmente 5-15 segundos)
5. **Leia a resposta** que aparecerá destacada em verde

## 💡 Dicas para fazer boas perguntas

### ✅ Perguntas eficazes:

- **Específicas:** "Qual é a data do contrato?"
- **Diretas:** "Quem é o autor do documento?"
- **Factuais:** "Qual é o valor total mencionado?"
- **Contextualizadas:** "Quais são as principais conclusões do estudo?"

### ❌ Evite perguntas:

- **Muito vagas:** "O que tem aqui?"
- **Fora do contexto:** "Qual é a capital da França?" (se não estiver no documento)
- **Múltiplas questões:** "Qual é a data e o valor e quem assinou?"
- **Opinativas:** "Este documento é bom?"

### 🎯 Exemplos de perguntas por tipo de documento:

**Contratos:**
- "Qual é a data de vigência do contrato?"
- "Quem são as partes envolvidas?"
- "Qual é o valor do acordo?"

**Artigos científicos:**
- "Qual é a metodologia utilizada?"
- "Quais são as principais conclusões?"
- "Quantos participantes teve o estudo?"

**Relatórios financeiros:**
- "Qual foi o lucro líquido?"
- "Qual é a receita total?"
- "Quais são os principais custos?"

**Manuais:**
- "Como instalar o produto?"
- "Quais são os requisitos do sistema?"
- "Onde encontrar suporte técnico?"

## ⚙️ Opções Avançadas

### Escolha do modelo de IA

No menu **"⚙️ Opções Avançadas"**, você pode selecionar diferentes modelos:

| Modelo | Velocidade | Qualidade | Custo | Recomendado para |
|--------|-----------|-----------|-------|------------------|
| **gpt-4.1-mini** | Média | Alta | Médio | Uso geral (padrão) |
| **gpt-4.1-nano** | Rápida | Boa | Baixo | Perguntas simples |
| **gemini-2.5-flash** | Rápida | Alta | Médio | Alternativa ao GPT |

**Quando usar cada modelo:**

- **gpt-4.1-mini:** Perguntas complexas, análises detalhadas
- **gpt-4.1-nano:** Perguntas simples, extração de dados básicos
- **gemini-2.5-flash:** Quando quiser uma segunda opinião ou alternativa

## 📊 Entendendo os resultados

### Tipos de resposta

1. **Resposta direta:**
   ```
   "A data do contrato é 15 de março de 2024."
   ```

2. **Resposta com contexto:**
   ```
   "De acordo com a seção 3.2, o valor total é de R$ 150.000,00, 
   dividido em 12 parcelas mensais."
   ```

3. **Resposta não encontrada:**
   ```
   "Não foi possível encontrar uma resposta no contexto fornecido."
   ```

### Validação de respostas

**Sempre:**
1. ✅ Verifique se a resposta faz sentido
2. ✅ Compare com o texto original (na visualização por página)
3. ✅ Considere o contexto do documento
4. ✅ Faça perguntas complementares se necessário

**Nunca:**
1. ❌ Confie cegamente na resposta sem validação
2. ❌ Use para decisões críticas sem verificação manual
3. ❌ Assuma que o OCR é 100% preciso

## 🔍 Solução de problemas comuns

### Problema: "OCR não extraiu o texto corretamente"

**Causas possíveis:**
- Qualidade ruim do PDF (baixa resolução)
- Texto manuscrito (OCR funciona melhor com texto impresso)
- Idioma não suportado
- Formatação complexa

**Soluções:**
1. Use um PDF de melhor qualidade
2. Tente reprocessar o arquivo
3. Verifique se o idioma está correto (padrão: inglês)
4. Para textos manuscritos, considere transcrever manualmente

### Problema: "Resposta não faz sentido"

**Causas possíveis:**
- Pergunta ambígua
- Informação não está no documento
- Contexto truncado (documento muito grande)

**Soluções:**
1. Reformule a pergunta de forma mais específica
2. Verifique se a informação realmente está no documento
3. Divida documentos muito grandes em partes menores
4. Tente um modelo diferente

### Problema: "Processamento muito lento"

**Causas possíveis:**
- Documento muito grande
- Muitas páginas
- Servidor sobrecarregado

**Soluções:**
1. Divida o documento em partes menores
2. Processe um arquivo por vez
3. Aguarde alguns minutos e tente novamente
4. Use PDFs com menos páginas

### Problema: "Arquivo não carrega"

**Causas possíveis:**
- Arquivo maior que 1 GB
- Formato não suportado
- PDF corrompido

**Soluções:**
1. Verifique o tamanho do arquivo
2. Certifique-se de que é um PDF válido
3. Tente comprimir o PDF
4. Use uma ferramenta para reparar o PDF

## 📁 Onde encontrar os arquivos gerados

### Logs de OCR

**Localização:** `/home/ubuntu/ocr_logs/`

**Conteúdo:**
- Texto extraído de cada página
- Organizado por documento
- Formato: `nome_do_arquivo.txt`

**Uso:**
- Verificar precisão do OCR
- Copiar texto extraído
- Análise manual do conteúdo

### Histórico de perguntas

**Localização:** `/home/ubuntu/todo.md`

**Conteúdo:**
- Nome dos arquivos processados
- Número de páginas
- Perguntas feitas
- Respostas recebidas
- Data e hora de cada consulta

**Uso:**
- Rastrear consultas anteriores
- Auditar uso do sistema
- Referência futura

## 🎓 Casos de uso práticos

### 1. Análise de contratos

**Cenário:** Você tem 50 contratos para revisar

**Fluxo:**
1. Upload de todos os contratos
2. Para cada contrato, pergunte:
   - "Qual é a data de vencimento?"
   - "Qual é o valor total?"
   - "Quais são as cláusulas de rescisão?"
3. Compare as respostas
4. Identifique contratos que precisam atenção

### 2. Pesquisa acadêmica

**Cenário:** Revisão de literatura científica

**Fluxo:**
1. Upload de artigos relevantes
2. Para cada artigo, pergunte:
   - "Qual é a metodologia?"
   - "Quais são os principais resultados?"
   - "Quais são as limitações?"
3. Compile as respostas em uma tabela
4. Use para escrever sua revisão

### 3. Análise financeira

**Cenário:** Análise de demonstrações financeiras

**Fluxo:**
1. Upload de relatórios financeiros
2. Extraia dados chave:
   - "Qual é a receita total?"
   - "Qual é o lucro líquido?"
   - "Quais são os principais custos?"
3. Compare entre períodos
4. Gere insights

### 4. Compliance e auditoria

**Cenário:** Verificação de conformidade

**Fluxo:**
1. Upload de documentos regulatórios
2. Verifique requisitos:
   - "Quais são os requisitos de segurança?"
   - "Quais certificações são necessárias?"
   - "Quais são os prazos?"
3. Crie checklist de conformidade
4. Identifique gaps

## 🔐 Segurança e privacidade

### Seus dados estão seguros:

- ✅ Arquivos processados localmente
- ✅ Textos não são armazenados permanentemente (apenas logs locais)
- ✅ Comunicação via HTTPS
- ✅ API keys protegidas

### Boas práticas:

- 🔒 Não faça upload de documentos ultra-confidenciais em ambientes compartilhados
- 🔒 Limpe os logs regularmente se contiverem informações sensíveis
- 🔒 Use em ambiente privado para documentos confidenciais
- 🔒 Verifique as políticas de privacidade da plataforma de hosting

## 📞 Suporte e ajuda

### Precisa de ajuda?

1. **Consulte este guia** primeiro
2. **Verifique a seção de troubleshooting**
3. **Revise os logs** para mensagens de erro
4. **Entre em contato** com o administrador do sistema

### Feedback

Sua opinião é importante! Se você:
- Encontrou um bug
- Tem uma sugestão de melhoria
- Precisa de uma funcionalidade nova
- Quer compartilhar um caso de sucesso

**Entre em contato** ou abra uma issue no GitHub.

## 🎉 Dicas finais

1. **Comece pequeno:** Teste com um documento simples primeiro
2. **Valide sempre:** Confira as respostas com o texto original
3. **Seja específico:** Perguntas claras geram respostas melhores
4. **Use os logs:** Eles são úteis para referência futura
5. **Experimente modelos:** Cada modelo tem seus pontos fortes
6. **Seja paciente:** OCR pode demorar em documentos grandes

---

**Aproveite o sistema e boa sorte com suas análises!** 🚀

*Última atualização: 23 de outubro de 2025*

