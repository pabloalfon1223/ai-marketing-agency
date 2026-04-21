#!/bin/bash

# Script automatizado para deployar Polt Mobilier a Railway
# Uso: bash deploy-railway.sh

set -e

echo "🚀 Iniciando deployment de Polt Mobilier a Railway..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/Procfile" ]; then
    echo "❌ Error: Ejecutar este script desde la raíz del proyecto"
    exit 1
fi

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir headers
print_section() {
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "  $1"
    echo "════════════════════════════════════════════════════════════"
}

print_section "PASO 1: Validar dependencias"
echo "✓ Railway CLI"
railway --version

echo "✓ Node.js"
node --version

echo "✓ npm"
npm --version

echo "✓ Git"
git --version

print_section "PASO 2: Autenticarse con Railway"
echo "⚠️  Se abrirá tu navegador para autenticarte con Railway"
echo "Presiona ENTER para continuar..."
read

railway login

print_section "PASO 3: Crear/Seleccionar proyecto en Railway"
echo "Selecciona tu proyecto o crea uno nuevo"
echo "Presiona ENTER para continuar..."
read

cd backend

# Inicializar Railway en el directorio backend
echo "Inicializando Railway..."
railway init

print_section "PASO 4: Configurar variables de entorno"
echo "Necesitamos agregar estas variables en Railway:"
echo ""
echo "📝 Variables necesarias:"
echo "  - ANTHROPIC_API_KEY: Tu clave de API de Anthropic"
echo "  - CORS_ORIGINS: Ya la configuramos a https://ai-marketing-agency.vercel.app,http://localhost:5173"
echo "  - GOOGLE_SHEETS_ID: ID de tu Google Sheet"
echo "  - GOOGLE_CREDENTIALS_JSON: Credenciales de Google (formato JSON)"
echo ""
echo "Abre https://railway.app/dashboard en tu navegador y agrega estas variables en el proyecto"
echo "Variables CORS_ORIGINS y DATABASE_URL se auto-detectan"
echo ""
echo "Presiona ENTER cuando hayas agregado las variables..."
read

print_section "PASO 5: Deploy del Backend"
echo "Deployando backend a Railway..."
railway up

echo ""
echo "✅ Backend deployado a Railway"
echo ""
echo "Para obtener la URL del backend:"
echo "  railway status"
echo ""

cd ..

print_section "PASO 6: Configurar variables en Vercel"
echo "Ahora necesitamos agregar la URL del backend a Vercel"
echo ""
echo "1. Obtén la URL de tu backend ejecutando en el directorio backend:"
echo "   railway status"
echo ""
echo "2. Luego ejecuta:"
echo "   vercel env add VITE_API_URL"
echo "   (Pega la URL del backend, ej: https://backend-abc123.railway.app)"
echo ""
echo "3. Y:"
echo "   vercel env add VITE_WS_URL"
echo "   (Pega: wss://[tu-url-railway])"
echo ""
echo "4. Finalmente redeploy:"
echo "   vercel --prod"
echo ""
echo "Presiona ENTER para continuar..."
read

print_section "Próximos pasos:"
echo ""
echo "✅ Backend deployado a Railway"
echo "⏳ Próximo: Agregar variables de entorno a Vercel"
echo ""
echo "Ejecuta estos comandos:"
echo ""
echo "  # Obtén la URL del backend"
echo "  cd backend && railway status && cd .."
echo ""
echo "  # Agrega variables a Vercel"
echo "  vercel env add VITE_API_URL"
echo "  vercel env add VITE_WS_URL"
echo ""
echo "  # Redeploy frontend"
echo "  vercel --prod"
echo ""

print_section "¡Listo!"
echo ""
echo "🎉 Tu aplicación Polt Mobilier está casi lista!"
echo ""
echo "Frontend: https://ai-marketing-agency.vercel.app"
echo "Backend Docs: https://[tu-backend-railway]/docs"
echo ""
