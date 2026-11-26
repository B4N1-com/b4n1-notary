5d34ce69-98ad-4822-b84a-3c8a9e923d08
# b4n1-Notar

Beweisen Sie, was Sie wann geliefert haben.

b4n1-Notar versiegelt ein Projekt in einem Merkle-Root und schreibt eine tragbare Proof-Datei. Überprüfen Sie es später oder geben Sie es einem Kunden weiter, und die Antwort ist eine einzige Zeile: verifiziert oder die erste Datei, die nicht mehr übereinstimmt.

## Warum es wichtig ist

Die Versionskontrolle zeichnet auf, was sich geändert hat. Es wird nicht aufgezeichnet, was genau Sie an einem bestimmten Tag geliefert haben: Ein Tag kann verschoben und ein Archiv erneut komprimiert werden. Ein Merkle-Wurzel über jeder Datei mit einem Zeitstempel ist ein Beweis, der nicht davon abhängt, dass man der Person vertraut, die sie erstellt hat.

## Installieren

- Python: pip install b4n1-notary
- JavaScript: npm install b4n1-notary
- Java: com.b4n1:b4n1-notary:0.2.0
- .NET: Dotnet-Paket B4n1.Notary hinzufügen
- Ruby: gem install b4n1-notary
- PHP: Komponist benötigt b4n1/b4n1-Notar
- Los: Holen Sie sich github.com/B4N1-com/b4n1-notary/sdks/go

Jedes Paket enthält vorkompilierte Binärdateien für Linux, macOS und Windows. Es ist kein Compiler erforderlich und es muss nichts anderes installiert werden.

## Was Sie tun können

- Einen Baum versiegeln: Der Stempel druckt die Dateianzahl, die Merkle-Wurzel und den Proof-Pfad.
- Später überprüfen: „Verifizieren“ berechnet die Wurzel neu und benennt etwaige Nichtübereinstimmungen.
- Anker in Bitcoin: verify-ots prüft den OpenTimestamps-Beleg mit eingegebenen Exit-Codes.
- Audit-Verlauf: Der Verlauf listet alle bereits versiegelten Nachweise auf.

## Lizenzierung

Die SDK-Wrapper sind Business Source License 1.1. Jede Binärdatei wird mit einer eigenen EULA verteilt.
