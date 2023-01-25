

def migrade_db(db,app):
    db.init_app(app)
    from fileStorage.models import User
    with app.app_context():
        db.create_all()


def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0