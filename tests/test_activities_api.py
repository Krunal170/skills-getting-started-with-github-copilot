from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_contains_known_activity():
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    assert 'Chess Club' in data


def test_signup_success_and_duplicate():
    activity = 'Chess Club'
    email = 'test_student@mergington.edu'

    # Ensure email not already present
    if email in activities[activity]['participants']:
        activities[activity]['participants'].remove(email)

    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    json = resp.json()
    assert 'Signed up' in json['message']
    assert email in activities[activity]['participants']

    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400

    # Cleanup
    activities[activity]['participants'].remove(email)


def test_unregister_success_and_not_registered():
    activity = 'Programming Class'
    email = 'unregister_test@mergington.edu'

    # Ensure email is present
    if email not in activities[activity]['participants']:
        activities[activity]['participants'].append(email)

    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200
    data = resp.json()
    assert 'Unregistered' in data['message']
    assert email not in activities[activity]['participants']

    # Unregistering again should fail
    resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp2.status_code == 400
