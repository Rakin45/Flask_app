import pytest
from webapp import create_app, db 
from webapp.models import Location


@pytest.fixture()
def app():
    app = create_app("sqlite://")

    with app.app_context():
        db.create_all()
        db.session.add_all([
            Location(location_name="SAVANNAH RIVER I-95 NEAR PORT WENTWORTH, GA",latitude=32.2354722,longitude=-81.1510833),
            Location(location_name="SAVANNAH RIVER AT GA 25, AT PORT WENTWORTH, GA",latitude=32.16533333,longitude=-81.1549167),

        ])
        db.session.commit()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()