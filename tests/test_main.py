def test_home_route(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Job Tracker API is running"


def test_register_user(client):
    response = client.post(
        "/register/",
        json={
            "name": "Zarif",
            "email": "zarif@example.com",
            "password": "zarif123"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Zarif"
    assert data["email"] == "zarif@example.com"
    assert "id" in data
    assert "hashed_password" not in data


def test_duplicate_email_register(client):
    user_data = {
        "name": "Zarif",
        "email": "zarif@example.com",
        "password": "zarif123"
    }

    first_response = client.post("/register/", json=user_data)
    second_response = client.post("/register/", json=user_data)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "email already registered"


def test_login_user(client):
    client.post(
        "/register/",
        json={
            "name": "Zarif",
            "email": "zarif@example.com",
            "password": "zarif123"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "zarif@example.com",
            "password": "zarif123"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user_me(client):
    client.post(
        "/register/",
        json={
            "name": "Zarif",
            "email": "zarif@example.com",
            "password": "zarif123"
        }
    )

    login_response = client.post(
        "/login",
        data={
            "username": "zarif@example.com",
            "password": "zarif123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Zarif"
    assert data["email"] == "zarif@example.com"

def get_auth_headers(client):
    client.post(
        "/register/",
        json={
            "name": "Zarif",
            "email": "zarif@example.com",
            "password": "zarif123"
        }
    )

    login_response = client.post(
        "/login",
        data={
            "username": "zarif@example.com",
            "password": "zarif123"
        }
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

def test_create_company(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/companies/",
        json={
            "name": "Google",
            "website": "https://careers.google.com",
            "location": "London",
            "industry": "Technology"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Google"
    assert data["website"] == "https://careers.google.com"
    assert data["location"] == "London"
    assert data["industry"] == "Technology"
    assert "id" in data
    assert "user_id" in data


def test_get_companies(client):
    headers = get_auth_headers(client)

    client.post(
        "/companies/",
        json={
            "name": "Google",
            "website": "https://careers.google.com",
            "location": "London",
            "industry": "Technology"
        },
        headers=headers
    )

    response = client.get(
        "/companies/",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Google"


def test_companies_requires_login(client):
    response = client.get("/companies/")

    assert response.status_code == 401