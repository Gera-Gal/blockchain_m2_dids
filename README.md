# blockchain_m2_dids
## Aplicación de escritorio para gestión de identidad descentralizada

## Identificadores Descentralizados (DIDs)
Con este prototipo actualmente puedes cargar la imagen de una credencial de elector y extraer el nombre, el cual se utiliza como metadata en la interacción con un smart contract desplegado en la red de Polygon Mainnet, con dicha interacción se genera un DID ocultando el contenido o texto en claro.

### Ejecución

Para poder probar la aplicación deberás incluir las variables:
- TATUM_API_KEY provista por tatum.io
- PRIVATE_KEY que corresponde a la llave privada de una cuenta en Polygon

Deberás contectar tu propia base de datos con una colección de "usuarios" que tenga la siguiente estructura:
```
_id: 66874be4d27e70535bff21e4
username: "gera"
password: "scrypt:32768:8:1$kzWmK4v9iDrG8fBF$bd5ef9afba6bd17bf87c35218a5012458a09…"
role: "user"
```

El modo de carga de datos más completo es "Carga documental" y el flujo concluye al generar el DID, mostrando el hash resultante en pantalla.

Se incluyen otros archivos para el trabajo a futuro de gestión de DIDs.

## Presentaciones Verificables (VPs)

También se incluyen archivos para la interacción con otro smart contract de VPs.
