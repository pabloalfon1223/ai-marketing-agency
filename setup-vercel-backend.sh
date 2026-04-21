#!/bin/bash

# Script para agregar URL del backend a Vercel y redeploy
# Uso: bash setup-vercel-backend.sh

set -e

echo "🚀 Configurando backend URL en Vercel..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "⚠️  Debes proporcionar la URL de tu backend de Railway"
    echo ""
    echo "Uso: bash setup-vercel-backend.sh https://tu-backend-url.railway.app"
    echo ""
    echo "Pasos:"
    echo "  1. Ve a Railway Dashboard"
    echo "  2. Abre tu proyecto"
    echo "  3. Click en 'Settings' → 'Domains'"
    echo "  4. Copia tu URL (ej: https://backend-abc123.railway.app)"
    echo "  5. Ejecuta este script con esa URL:"
    echo ""
    echo "     bash setup-vercel-backend.sh https://backend-abc123.railway.app"
    echo ""
    exit 1
fi

BACKEND_URL="$1"

# Validar URL
if [[ ! "$BACKEND_URL" =~ ^https?:// ]]; then
    echo "❌ Error: La URL debe empezar con http:// o https://"
    exit 1
fi

echo "✓ URL del backend: $BACKEND_URL"
echo ""

# Convertir HTTPS a WSS para WebSocket
WS_URL="${BACKEND_URL//https:/wss:/}"
WS_URL="${WS_URL//http:/ws:/}"

echo "✓ URL WebSocket: $WS_URL"
echo ""

# Verificar que Vercel CLI está autenticado
echo "Verificando autenticación con Vercel..."
USER=$(vercel whoami)
echo "✓ Autenticado como: $USER"
echo ""

# Ir al directorio frontend
cd frontend

echo "Agregando variables de entorno en Vercel..."
echo ""

# Agregar VITE_API_URL
echo "  • VITE_API_URL = $BACKEND_URL"
vercel env add VITE_API_URL << EOF
$BACKEND_URL
EOF

echo "  ✓ Agregada VITE_API_URL"
echo ""

# Agregar VITE_WS_URL
echo "  • VITE_WS_URL = $WS_URL"
vercel env add VITE_WS_URL << EOF
$WS_URL
EOF

echo "  ✓ Agregada VITE_WS_URL"
echo ""

cd ..

echo "════════════════════════════════════════════════════════════"
echo "  Redeploy del Frontend en Vercel"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Ejecutando: vercel --prod"
echo ""

cd frontend
vercel --prod
cd ..

echo ""
echo -e "${GREEN}✅ ¡Listo!${NC}"
echo ""
echo "Tu aplicación Polt Mobilier está completamente deployada:"
echo ""
echo "  Frontend: https://ai-marketing-agency.vercel.app"
echo "  Backend: $BACKEND_URL"
echo "  Backend Docs: $BACKEND_URL/docs"
echo ""
echo "Las variables de entorno han sido agregadas a Vercel y el frontend"
echo "ha sido redeploy automáticamente."
echo ""
echo "🎉 ¡La aplicación debería funcionar correctamente ahora!"
echo ""
