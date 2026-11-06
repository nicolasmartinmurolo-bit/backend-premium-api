"""
Suite de Pruebas Automatizadas para Endpoints de Usuarios y Autenticación.
--------------------------------------------------------------------------------
Este módulo implementa pruebas de integración para verificar el correcto 
funcionamiento del flujo de usuarios y seguridad:
1. Registro exitoso de nuevos usuarios y validación de salida de datos (exclusión de contraseñas).
2. Proceso de autenticación por OAuth2 (/login/access-token) y acceso seguro a rutas protegidas (/me).
"""

def test_create_user(client):
    """
    Prueba la creación de un nuevo usuario mediante una petición POST a /api/v1/users/:
    - Envía datos válidos en formato JSON.
    - Valida que el código de respuesta HTTP sea 200 (OK).
    - Comprueba que el JSON devuelto contenga el email correcto y el ID generado.
    - Verifica por seguridad estricta que NUNCA se devuelva el hash de la contraseña.
    """
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "password": "securepassword123",
            "full_name": "Test User",
            "is_active": True
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    # Verificación de seguridad clave: el campo hashed_password debe estar ausente en la respuesta.
    assert "hashed_password" not in data


def test_login_and_access_protected_route(client):
    """
    Prueba el flujo completo de autenticación y autorización (Stateful/Stateless flow):
    1. Registra un usuario de prueba en el sistema.
    2. Realiza una petición POST al endpoint de login enviando credenciales como formulario (OAuth2).
    3. Extrae y valida el token JWT obtenido en la respuesta.
    4. Utiliza el token Bearer en los headers para consumir la ruta protegida /api/v1/users/me.
    """
    # Paso 1: Creamos el usuario inicial en la base de datos de pruebas.
    client.post(
        "/api/v1/users/",
        json={
            "email": "auth@example.com",
            "password": "mypassword123",
            "full_name": "Auth User",
            "is_active": True
        },
    )

    # Paso 2: Solicitamos el token de acceso enviando los datos mediante formulario (OAuth2PasswordRequestForm).
    response = client.post(
        "/api/v1/login/access-token",
        data={
            "username": "auth@example.com",
            "password": "mypassword123"
        },
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    token = token_data["access_token"]

    # Paso 3: Consumimos la ruta protegida /me inyectando el token JWT en la cabecera 'Authorization'.
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/api/v1/users/me", headers=headers)
    
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == "auth@example.com"
    assert me_data["full_name"] == "Auth User"