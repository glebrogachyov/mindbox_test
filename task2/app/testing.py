from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root(result):
    response = client.get("/")
    assert response.status_code == 200
    if result:
        assert response.json() == result


def test_get_products(result=None):
    response = client.get("/get_products")
    assert response.status_code == 200
    if result:
        assert response.json() == result


def test_get_categories(result=None):
    response = client.get("/get_categories")
    assert response.status_code == 200
    if result:
        assert response.json() == result


def test_get_products_to_categories(result=None):
    response = client.get("/get_products_to_categories")
    assert response.status_code == 200
    if result:
        assert response.json() == result


def test_init_table(result=None):
    response = client.get("/db_init_table")
    assert response.status_code == 200
    if result:
        assert response.json() == result


if __name__ == '__main__':
    test_root("Hello!")
    test_get_products("error. table doesn't exist.")
    test_get_categories("error. table doesn't exist.")
    test_get_products_to_categories("error. table doesn't exist.")
    test_init_table("done.")
    test_get_products()
    test_get_categories()
    test_get_products_to_categories()


