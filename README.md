# WhatsApp Chat Analysis Tool

Uma ferramenta interativa para análise de conversas do WhatsApp, construída com Streamlit. Visualize padrões de mensagens e obtenha insights sobre suas conversas.

![como funciona](https://github.com/maluta/maluta.github.com/blob/master/images/whatsapp-history-ai_output.gif?raw=true)

## 🌟 Funcionalidades

- 🤖 Análise de conversas usando IA generaiva (via Google Gemini API) ★
- 📊 Visualização da distribuição de mensagens por hora do dia
- 📅 Visualização da distribuição de mensagens por dia da semana
- 📅 Filtro de mensagens por período

## 📋 Pré-requisitos

```
python 3.7+
```

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/maluta/whatsapp-analysis.git
cd whatsapp-analysis
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure sua chave API do Google:
   - Crie um arquivo `config.yaml` na raiz do projeto 
   - Adicione sua chave API:
     ```yaml
     GOOGLE_API_KEY: "sua-chave-api-aqui"
     ```

   [OPCIONAL] Outra alternativa é renomear o arquivo `config.yaml.example` para `config.yaml`
   ```bash
   mv config.yaml.example config.yaml
   ```

## 🚀 Como Usar

1. Execute o aplicativo:
```bash
streamlit run app.py
```

2. No navegador:
   - Faça upload do arquivo ZIP da conversa do WhatsApp 
   - Selecione o período de análise
   - Clique em "Analisar Chat"

3. Exportando conversas do WhatsApp ([veja como exportar](https://faq.whatsapp.com/1180414079177245/?cms_platform=android))
   - Abra a conversa no WhatsApp
   - Menu > Mais > Exportar conversa
   - Escolha "Sem mídia"
   - Salve o arquivo ZIP

## 📊 Visualizações

### Distribuição por Hora
Mostra quantas mensagens foram enviadas em cada hora do dia, permitindo identificar os horários mais ativos da conversa.

### Distribuição por Dia da Semana
Apresenta o volume de mensagens para cada dia da semana, revelando padrões de uso ao longo da semana.

## 🤖 Análise com IA
O aplicativo utiliza a API do Google Generative AI para fornecer insights adicionais sobre as conversas. Para usar esta funcionalidade, certifique-se de configurar corretamente sua chave API no arquivo `config.yaml`.

## 📝 Notas

- Os arquivos de conversa devem estar no formato ZIP exportado diretamente do WhatsApp
- Certifique-se de que o arquivo ZIP contém apenas o arquivo de texto da conversa
- Para melhores resultados, use conversas com pelo menos uma semana de dados

## 🔒 Privacidade

Este aplicativo processa todas as conversas localmente em seu computador. Nenhum dado é enviado para servidores externos, exceto quando a análise de IA é solicitada (usando a API do Google).

**IMPORTANTE: nos [Termos de Serviço adicionais da API Gemini](https://ai.google.dev/gemini-api/terms?hl=pt-br) é expressamente recomendado não enviar informações sensíveis, confidenciais ou pessoais ao utilizar os Serviços Não Pagos.** 

Por exemplo, se você gerar a chave de API [usando o Google AI Studio](https://aistudio.google.com/apikey) sem ativar faturamento (como ao gerar uma chave sem adicionar um método de pagamento), você está utilizando, em princípio, um Serviço Não Pago, sujeito a políticas diferentes. Nos Serviços Não Pagos, o Google pode usar os dados fornecidos para melhorar seus produtos e serviços.

Veja o trecho abaixo extraido dos termos de serviço:

```
Uso de dados para Serviços Não Pagos
Os termos nesta seção se aplicam exclusivamente ao seu uso de Serviços Não Pagos.

A licença que você concede ao Google de acordo com a seção "Envio de conteúdo" nos Termos das APIs também se estende, na medida exigida pela legislação aplicável, ao nosso uso, a qualquer conteúdo (por exemplo, comandos, incluindo instruções de sistema, conteúdo armazenado em cache e arquivos como imagens, vídeos ou documentos associados) que você envia aos Serviços e a qualquer resposta gerada. O Google usa esses dados, de acordo com nossa Política de Privacidade, para fornecer, melhorar e desenvolver nossos produtos, serviços e tecnologias de aprendizado de máquina, incluindo os recursos, produtos e serviços empresariais do Google.

Para fins de qualidade e aprimoramento dos nossos produtos, revisores humanos podem ler, fazer anotações e processar suas entradas e saídas das APIs. O Google toma medidas para proteger sua privacidade como parte desse processo. Isso inclui desassociar esses dados da sua Conta do Google, chave de API e projeto do Cloud antes que sejam vistos ou anotados por revisores. Não envie informações sensíveis, confidenciais ou pessoais para os Serviços Não Pagos.

O Google só usa conteúdo que você importa ou faz upload no nosso recurso de ajustes de modelos para esse objetivo explícito. Os ajustes de conteúdo podem ser retidos em conexão com seus modelos ajustados para fins de reajuste quando os modelos compatíveis são mudados. Quando você exclui um modelo ajustado, o conteúdo de ajustes relacionado também é removido.
```

Já nos Termos de Serviço adicionais da API Gemini, **o Google especifica práticas distintas para o uso de dados em Serviços Pagos**. Ao utilizar esses serviços, **o Google não emprega seus comandos (incluindo instruções de sistema, conteúdo em cache e arquivos como imagens, vídeos ou documentos associados) ou respostas para aprimorar seus produtos.**

## 📄 Licença

O código-fonte deste projeto está sob a Licença MIT. Veja o arquivo LICENSE para obter mais detalhes. No entanto, lembre-se de que algumas funcionalidades dependem de serviços de terceiros que têm suas próprias condições de uso.

Por exemplo, algumas funcionalidades deste aplicativo depende de serviços de IA generativa fornecidos pela API do Google Gemini. Para usar o aplicativo, você precisará configurar seu próprio acesso à API do Google, o que implica aceitar os Termos de Serviço do Google.

##  Feito por [Tiago Maluta](https://maluta.github.io)

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues para sugerir melhorias e correções.