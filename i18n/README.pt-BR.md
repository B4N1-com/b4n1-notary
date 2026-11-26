7445ea80-c834-4eab-aa62-64b34991869b
#b4n1-notário

Prove o que você entregou e quando.

b4n1-notary sela um projeto em uma raiz Merkle e grava um arquivo de prova portátil. Verifique mais tarde, ou entregue a um cliente, e a resposta será uma única linha: verificado ou o primeiro arquivo que não corresponde mais.

## Por que é importante

O controle de versão registra o que mudou. Ele não registra exatamente o que você entregou em um determinado dia: uma tag pode ser movida e um arquivo pode ser compactado novamente. Uma raiz Merkle sobre cada arquivo, com carimbo de data/hora, é uma evidência que não depende da confiança da pessoa que o produziu.

## Instalar

- Python: pip install b4n1-notário
- JavaScript: npm install b4n1-notário
- Java: com.b4n1:b4n1-notário:0.2.0
- .NET: dotnet adiciona pacote B4n1.Notary
- Ruby: gem install b4n1-notário
- PHP: compositor requer b4n1/b4n1-notary
- Vá: acesse github.com/B4N1-com/b4n1-notary/sdks/go

Cada pacote contém binários pré-compilados para Linux, macOS e Windows. Nenhum compilador é necessário e não há mais nada para instalar.

## O que você pode fazer

- Selar uma árvore: o carimbo imprime a contagem de arquivos, a raiz Merkle e o caminho da prova.
- Verificar mais tarde: verificar recalcula a raiz e nomeia qualquer incompatibilidade.
- Âncora em Bitcoin: verify-ots verifica o recibo do OpenTimestamps com códigos de saída digitados.
- Histórico de auditoria: o histórico lista todas as provas já lacradas.

## Licenciamento

Os wrappers do SDK são Business Source License 1.1. Cada binário é distribuído com seu próprio EULA.
