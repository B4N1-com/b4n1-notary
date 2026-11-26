6af9b826-84e9-4b71-9d81-deff003487e4
#b4n1-notaire

Prouvez ce que vous avez livré et quand.

b4n1-notary scelle un projet dans une racine Merkle et écrit un fichier de preuve portable. Vérifiez-le plus tard, ou remettez-le à un client, et la réponse est une seule ligne : vérifié, ou le premier fichier qui ne correspond plus.

## Pourquoi c'est important

Le contrôle de version enregistre ce qui a changé. Il n'enregistre pas exactement ce que vous avez livré un jour donné : un tag peut bouger et une archive peut être recompressée. Une racine Merkle sur chaque fichier, avec un horodatage, est une preuve qui ne dépend pas de la confiance de la personne qui l'a produit.

## Installer

- Python : pip install b4n1-notaire
- JavaScript : npm install b4n1-notary
- Java : com.b4n1:b4n1-notaire:0.2.0
- .NET : dotnet ajoute le package B4n1.Notary
- Ruby : installation de gemmes b4n1-notary
- PHP : le compositeur nécessite b4n1/b4n1-notary
- Allez : allez chercher github.com/B4N1-com/b4n1-notary/sdks/go

Chaque package contient des binaires précompilés pour Linux, macOS et Windows. Aucun compilateur n'est nécessaire et il n'y a rien d'autre à installer.

## Ce que vous pouvez faire

- Sceller un arbre : le tampon imprime le nombre de fichiers, la racine Merkle et le chemin de preuve.
- Vérifier plus tard : verify recalcule la racine et nomme toute incompatibilité.
- Ancre dans Bitcoin : verify-ots vérifie le reçu OpenTimestamps avec les codes de sortie saisis.
- Historique d'audit : l'historique répertorie toutes les preuves déjà scellées.

## Licences

Les wrappers du SDK sont Business Source License 1.1. Chaque binaire est distribué avec son propre CLUF.
