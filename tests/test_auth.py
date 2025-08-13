import pytest
from httpx import AsyncClient

from app.main import app

#
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app,base_url='http://test') as client:
        yield client


@pytest.mark.asyncio
async def test_register(db_session):
    response = await async_client.post('/register', json={
        'name': 'test_user',
        'email': 'test@example.com',
        'password': '12345'
    })

    assert response.status_code == 201
    data = response.json()
    assert data['email'] == 'test@example.com'