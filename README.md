# Canariaswebconsulta

Plataforma web para clínica de estética con backend en Python (Django/FastAPI) y frontend React responsive. Dispone de tres roles (admin, personal y cliente). Permite gestionar fichas clínicas con datos obligatorios, histórico de tratamientos y observaciones, además de un calendario centralizado para planificar, modificar ...

## Configuración de variables de entorno del frontend

Para el desarrollo local, copia el archivo de ejemplo y ajusta los valores según tu entorno:

```bash
cp frontend/.env.example frontend/.env.local
```

El archivo `frontend/.env.example` incluye las variables mínimas necesarias:

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_DEFAULT_THEME=light
VITE_DEMO_MODE=false
```

Usa `VITE_DEFAULT_THEME` para fijar el tema inicial (por ejemplo `light` u `dark`) y `VITE_DEMO_MODE` para activar o desactivar funcionalidades de demostración.
