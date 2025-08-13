import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.deps.dependes import get_db
from app.main import app

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/myapp_test"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
def override_get_db(db_session):
    async def _get_db_override():
        yield db_session
    app.dependency_overrides[get_db] = _get_db_override
