def test_auth_contract():
    from app.routes import auth
    assert hasattr(auth,'router')
