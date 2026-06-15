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


def create_test_company(client, headers):
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
    return response.json()


def create_test_application(client, headers):
    company = create_test_company(client, headers)

    response = client.post(
        "/applications/",
        json={
            "company_id": company["id"],
            "job_title": "Backend Developer",
            "job_type": "full-time",
            "location": "London",
            "remote": True,
            "salary_min": 28000,
            "salary_max": 40000,
            "currency": "GBP",
            "status": "applied",
            "source": "LinkedIn",
            "job_url": "https://linkedin.com/jobs/example-backend",
            "applied_date": "2026-06-15T10:00:00",
            "deadline": "2026-07-15T23:59:00",
            "priority": "high"
        },
        headers=headers
    )

    assert response.status_code == 200
    return response.json()


def test_create_application(client):
    headers = get_auth_headers(client)

    application = create_test_application(client, headers)

    assert application["job_title"] == "Backend Developer"
    assert application["job_type"] == "full-time"
    assert application["location"] == "London"
    assert application["remote"] is True
    assert application["status"] == "applied"
    assert application["priority"] == "high"
    assert "id" in application
    assert "user_id" in application
    assert "company_id" in application


def test_get_applications(client):
    headers = get_auth_headers(client)

    create_test_application(client, headers)

    response = client.get(
        "/applications/",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Applications fetched successfully"
    assert data["count"] == 1
    assert data["applications"][0]["job_title"] == "Backend Developer"


def test_application_summary(client):
    headers = get_auth_headers(client)

    create_test_application(client, headers)

    response = client.get(
        "/applications/summary",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_applications"] == 1
    assert data["applied_count"] == 1
    assert data["remote_count"] == 1
    assert data["high_priority_count"] == 1


def test_applications_requires_login(client):
    response = client.get("/applications/")

    assert response.status_code == 401


def test_create_interview(client):
    headers = get_auth_headers(client)

    application = create_test_application(client, headers)

    response = client.post(
        "/interviews/",
        json={
            "application_id": application["id"],
            "interview_type": "technical interview",
            "scheduled_at": "2026-06-25T14:00:00",
            "location_or_link": "https://meet.google.com/example",
            "interviewer_name": "Sarah Ahmed",
            "status": "scheduled",
            "notes": "Prepare FastAPI, SQLAlchemy, PostgreSQL, and authentication."
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["application_id"] == application["id"]
    assert data["interview_type"] == "technical interview"
    assert data["status"] == "scheduled"
    assert data["interviewer_name"] == "Sarah Ahmed"
    assert "id" in data


def test_get_interviews(client):
    headers = get_auth_headers(client)

    application = create_test_application(client, headers)

    client.post(
        "/interviews/",
        json={
            "application_id": application["id"],
            "interview_type": "technical interview",
            "scheduled_at": "2026-06-25T14:00:00",
            "location_or_link": "https://meet.google.com/example",
            "interviewer_name": "Sarah Ahmed",
            "status": "scheduled",
            "notes": "Prepare FastAPI, SQLAlchemy, PostgreSQL, and authentication."
        },
        headers=headers
    )

    response = client.get(
        "/interviews/",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["interview_type"] == "technical interview"


def test_interviews_requires_login(client):
    response = client.get("/interviews/")

    assert response.status_code == 401


def test_create_application_note(client):
    headers = get_auth_headers(client)

    application = create_test_application(client, headers)

    response = client.post(
        "/application-notes/",
        json={
            "application_id": application["id"],
            "note": "Recruiter replied and moved me to technical interview stage."
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["application_id"] == application["id"]
    assert data["note"] == "Recruiter replied and moved me to technical interview stage."
    assert "id" in data


def test_get_application_notes(client):
    headers = get_auth_headers(client)

    application = create_test_application(client, headers)

    client.post(
        "/application-notes/",
        json={
            "application_id": application["id"],
            "note": "Recruiter replied and moved me to technical interview stage."
        },
        headers=headers
    )

    response = client.get(
        "/application-notes/",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["note"] == "Recruiter replied and moved me to technical interview stage."


def test_application_notes_requires_login(client):
    response = client.get("/application-notes/")

    assert response.status_code == 401



