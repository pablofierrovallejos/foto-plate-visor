# Google OAuth Setup Guide

## Configuración de Google OAuth para Login

### 1. Crear un proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google Identity

### 2. Configurar OAuth 2.0

1. Ve a **APIs & Services** > **Credentials**
2. Clic en **Create Credentials** > **OAuth 2.0 Client ID**
3. Configura la pantalla de consentimiento OAuth si no lo has hecho
4. Selecciona **Web application** como tipo de aplicación
5. Configura:
   - **Name**: Plate Track Talcahuano
   - **Authorized JavaScript origins**: 
     - `http://localhost:5000` (para desarrollo)
     - `https://tu-dominio.com` (para producción)
   - **Authorized redirect URIs**: 
     - `http://localhost:5000/auth/google` (para desarrollo)
     - `https://tu-dominio.com/auth/google` (para producción)

### 3. Obtener las credenciales

1. Copia el **Client ID** y **Client Secret**
2. Actualiza el archivo `config.py`:

```python
# Google OAuth configuration
GOOGLE_CLIENT_ID = "tu-client-id-aqui.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "tu-client-secret-aqui"
```

### 4. Configurar variables de entorno (recomendado)

Crea un archivo `.env` en la raíz del proyecto:

```
GOOGLE_CLIENT_ID=tu-client-id-aqui.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret-aqui
SECRET_KEY=tu-clave-secreta-super-segura
```

### 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 6. Configurar la aplicación Flask

Asegúrate de que tu aplicación Flask tenga configurada la clave secreta y las sesiones:

```python
app.config['SECRET_KEY'] = 'tu-clave-secreta-super-segura'
app.config['SESSION_TYPE'] = 'filesystem'
```

### 7. Funcionalidades implementadas

- **Login con Google**: Botón de "Iniciar sesión con Google"
- **Login tradicional**: Formulario de email/contraseña
- **Gestión de sesiones**: Mantenimiento de estado de usuario
- **Logout**: Cierre de sesión seguro
- **Protección de rutas**: Decorator para rutas que requieren autenticación

### 8. Rutas disponibles

- `/login` - Página de login
- `/auth/google` - Callback de Google OAuth
- `/auth/login` - Login tradicional
- `/logout` - Cerrar sesión
- `/profile` - Perfil de usuario (requiere autenticación)

### 9. Uso en templates

Para verificar si el usuario está logueado:

```html
{% if session.user %}
    <p>Bienvenido, {{ session.user.name }}!</p>
    <a href="{{ url_for('main.logout') }}">Cerrar sesión</a>
{% else %}
    <a href="{{ url_for('main.login') }}">Iniciar sesión</a>
{% endif %}
```

### 10. Consideraciones de seguridad

- Nunca expongas el Client Secret en el código frontend
- Usa HTTPS en producción
- Configura correctamente los dominios autorizados
- Mantén actualizada la clave secreta de Flask

### 11. Troubleshooting

- **Error 400**: Verifica que los dominios estén correctamente configurados
- **Token inválido**: Asegúrate de que el Client ID sea correcto
- **Sesión no persiste**: Verifica que SECRET_KEY esté configurada

## Ejemplo de configuración completa

```python
# config.py
import os

class Config:
    # ... otras configuraciones ...
    
    # Session configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # Google OAuth configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your-client-id.googleusercontent.com')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'your-client-secret')
```
