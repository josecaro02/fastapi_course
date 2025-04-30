from fastapi import status

def test_create_customer(client):
    response = client.post(
        '/customers',
        json={
            'name': 'Josefi',
            'email': 'josefi@caro.com',
            'age': 31,
            'description': 'holi!'
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

def test_read_customer(client):
    response = client.post(
        '/customers',
        json={
            'name': 'Josefi',
            'email': 'josefi@caro.com',
            'age': 31,
            'description': 'holi!'
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    customer_id : int = response.json()['id']
    response_read = client.get(
        f'/customer/{customer_id}'
    )
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()['name'] == "Josefi"
    