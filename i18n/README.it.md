8e91be9a-e7fe-4776-9225-509ccaee1269
#b4n1-notaio

Dimostra cosa hai consegnato e quando.

b4n1-notary sigilla un progetto in una radice Merkle e scrive un file di prova portatile. Verificalo più tardi, o consegnalo a un cliente, e la risposta è una sola riga: verificato, o il primo file che non corrisponde più.

## Perché è importante

Il controllo della versione registra ciò che è cambiato. Non registra cosa hai consegnato esattamente in un determinato giorno: un tag può spostarsi e un archivio può essere rezippato. Una radice Merkle su ogni file, con un timestamp, è una prova che non dipende dalla fiducia nella persona che lo ha prodotto.

## Installa

- Python: pip installa b4n1-notary
- JavaScript: npm installa b4n1-notary
- Java: com.b4n1:b4n1-notaio:0.2.0
- .NET: dotnet aggiunge il pacchetto B4n1.Notary
- Ruby: gem installa b4n1-notary
- PHP: il compositore richiede b4n1/b4n1-notary
- Vai: vai a prendere github.com/B4N1-com/b4n1-notary/sdks/go

Ogni pacchetto contiene binari precompilati per Linux, macOS e Windows. Non è necessario alcun compilatore e non c'è nient'altro da installare.

## Cosa puoi fare

- Sigilla un albero: il timbro stampa il conteggio dei file, la radice Merkle e il percorso della prova.
- Verifica più tardi: verifica ricalcola la radice e nomina eventuali discrepanze.
- Ancoraggio in Bitcoin: verify-ots controlla la ricevuta OpenTimestamps con i codici di uscita digitati.
- Cronologia dell'audit: la cronologia elenca tutte le prove già sigillate.

## Licenza

I wrapper SDK sono la licenza Business Source 1.1. Ogni binario è distribuito con il proprio EULA.
