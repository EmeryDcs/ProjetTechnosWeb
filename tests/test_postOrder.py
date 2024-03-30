from flask import *
import pytest
from mon_app import app as flask_app

@pytest.fixture(scope="module")
def app():
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture(scope="module")
def client(app):
    return app.test_client()

class TestPostOrder(object):
    def test_create_new_order(self, app, client):
        with app.app_context():
            data = {'product': {'id': 2, 'quantity': 1}}
            response = client.post("/order", json=data)
            assert response.status_code == 302
            #assert response.location == "/order/1"

    def test_order_ooi(self, app, client):
        with app.app_context():
            data = {'product': {'id': 4, 'quantity': 1}}
            response = client.post("/order", json=data)
            assert response.status_code == 422
            assert response.json == {
                "error": {
                    'product': {
                        "code": "out-of-inventory",
                        "name": "Le produit demandé n'est pas en inventaire."
                    }
                }
            }

    def test_affiche_order(self, app, client):
        with app.app_context():
            response = client.get("/order/1")
            assert response.status_code == 200
            #assert response.data == b'{"id": 1, "produit": 2, "quantite": 1}\n'