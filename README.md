# Laboratorio: gRPC + FastAPI + WebSocket

## Objetivo

Implementar una arquitectura de comunicación distribuida donde:

- un backend gRPC emite un stream de precios en tiempo real,
- un gateway FastAPI actúa como cliente gRPC,
- el frontend web recibe los datos mediante WebSockets y los visualiza en un dashboard.

## Estructura del proyecto

- `protobufs/crypto.proto`: contrato Protocol Buffers.
- `server.py`: servidor gRPC con streaming de datos.
- `web_app.py`: gateway FastAPI + WebSocket.
- `static/index.html`: dashboard web con Chart.js.
- `requirements.txt`: dependencias del laboratorio.

## Requisitos

- Python 3.12
- Entorno virtual recomendado

## Instalación

```powershell
cd "C:\Users\evach\OneDrive\Documentos\SISTEMAS\6to-semestre\Arquitectura_de_Software\LABORATORIOS\LAB_FastAPI_gRPC"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protobufs/crypto.proto
```

## Ejecución

### 1) Iniciar el servidor gRPC

```powershell
python server.py
```

### 2) Iniciar el gateway FastAPI

En otra terminal:

```powershell
cd "C:\Users\evach\OneDrive\Documentos\SISTEMAS\6to-semestre\Arquitectura_de_Software\LABORATORIOS\LAB_FastAPI_gRPC"
.\.venv\Scripts\Activate.ps1
python web_app.py
```

### 3) Abrir el dashboard

Abrir en el navegador:

```text
http://127.0.0.1:8001/
```

Escribir un ticker como `bitcoin`, `ethereum`, `solana` o `dogecoin` y pulsar `Conectar Stream`.

## Verificación funcional

Se comprobó que:

- el servidor gRPC responde con stream de datos,
- el gateway FastAPI sirve la UI y expone `/ws/crypto/{ticker}`,
- el navegador recibe mensajes JSON por WebSocket y actualiza la gráfica.

## Marco conceptual

### ¿Por qué un navegador no habla gRPC directamente?

Los navegadores no tienen soporte nativo para llamadas gRPC sobre HTTP/2 con protocolos binarios como lo hace un cliente Python. Por eso se usa un gateway FastAPI para consumir el servicio gRPC y convertir el flujo a WebSockets para el frontend.

### ¿Qué ventajas tiene Protocol Buffers frente a JSON?

- serialización binaria y más compacta,
- mejor rendimiento en transmisión de alta frecuencia,
- esquemas tipados con validación más estricta,
- menos overhead que JSON en datos intensivos.

### Diferencia entre gRPC server streaming y WebSocket

- gRPC server streaming: flujo unidireccional desde un backend hacia un cliente gRPC.
- WebSocket: protocolo de navegador para mantener una conexión bidireccional con el frontend web, útil para interfaces interactivas.

## Rubrica de cumplimiento

- [x] Definición del contrato `.proto`
- [x] Generación de stubs gRPC en Python
- [x] Servidor gRPC con streaming
- [x] Gateway FastAPI
- [x] WebSocket para frontend
- [x] Dashboard HTML/JS interactivo
- [x] Documentación y pasos de ejecución
- [x] Verificación funcional de flujo end-to-end

## Resultado esperado

El dashboard muestra el precio del activo seleccionado y actualiza la línea del gráfico en tiempo real.
