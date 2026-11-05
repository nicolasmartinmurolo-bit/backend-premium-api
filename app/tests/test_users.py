def test_create_user(client):
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
    # Verificamos por seguridad que nunca se devuelva el password hasheado
    assert "hashed_password" not in data

def test_login_and_access_protected_route(client):
    # 1. Primero creamos el usuario
    client.post(
        "/api/v1/users/",
        json={
            "email": "auth@example.com",
            "password": "mypassword123",
            "full_name": "Auth User",
            "is_active": True
        },
    )

    # 2. Hacemos login en el endpoint de acceso (OAuth2 usa form-data, por eso usamos 'data')
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

    # 3. Intentamos acceder a la ruta protegida /me pasando el token JWT en los headers
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/api/v1/users/me", headers=headers)
    
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == "auth@example.com"
    assert me_data["full_name"] == "Auth User"