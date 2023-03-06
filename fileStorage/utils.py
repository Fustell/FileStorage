

def migrade_db(db):
    "Import here all necessary models to migrate"
    from fileStorage.models import User
    db.create_all()


def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0