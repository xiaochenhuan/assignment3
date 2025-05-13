import pytest
from app import app
from app.db_models import db, User, HostStar, Planet
from flask import url_for

import pytest

@pytest.fixture(scope="module")
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()

# -------------------
# Model Tests
# -------------------
def test_user_model_password():
    user = User(username='test', email='test@example.com')
    user.set_password('abc123')
    assert user.check_password('abc123')
    assert not user.check_password('wrong')

def test_hoststar_planet_relationship():
    star = HostStar(hostname='StarA')
    planet = Planet(pl_name='PlanetA', host_star=star)
    assert planet.host_star.hostname == 'StarA'
    assert star.planets[0].pl_name == 'PlanetA'

# -------------------
# View Tests
# -------------------
def test_index_view(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Stellar and Planetary Data' in response.data
