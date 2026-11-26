8f6521ad-7a97-4664-98e9-6c4bb580d1a1
# b4n1-notario

Demuestre lo que entregó y cuándo.

b4n1-notary sella un proyecto en una raíz de Merkle y escribe un archivo de prueba portátil. Verifíquelo más tarde o entréguelo a un cliente y la respuesta será una sola línea: verificado o el primer archivo que ya no coincide.

## Por qué es importante

El control de versiones registra lo que cambió. No registra qué entregó exactamente en un día determinado: una etiqueta se puede mover y un archivo se puede volver a comprimir. Una raíz de Merkle sobre cada archivo, con una marca de tiempo, es evidencia que no depende de confiar en la persona que lo produjo.

## Instalar

- Python: pip instalar b4n1-notario
- JavaScript: npm instala b4n1-notario
- Java: com.b4n1:b4n1-notario:0.2.0
- .NET: dotnet agrega el paquete B4n1.Notary
- Ruby: instalación de gemas b4n1-notary
- PHP: el compositor requiere notario b4n1/b4n1
- Vaya: vaya a github.com/B4N1-com/b4n1-notary/sdks/go

Cada paquete incluye binarios precompilados para Linux, macOS y Windows. No se necesita ningún compilador y no hay nada más que instalar.

## Qué puedes hacer

- Sellar un árbol: el sello imprime el recuento de archivos, la raíz de Merkle y la ruta de prueba.
- Verificar más tarde: verificar vuelve a calcular la raíz y nombra cualquier discrepancia.
- Ancla en Bitcoin: verificar-ots verifica el recibo de OpenTimestamps con códigos de salida escritos.
- Historial de auditoría: el historial enumera todas las pruebas ya selladas.

## Licencias

Los contenedores del SDK son Business Source License 1.1. Cada binario se distribuye con su propio EULA.
