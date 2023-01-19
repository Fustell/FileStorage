

def migrade_db(db,app):
    db.init_app(app)
    from fileStorage.models import User
    with app.app_context():
        db.create_all()