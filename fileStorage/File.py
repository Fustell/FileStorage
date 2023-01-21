import uuid
import os

BASE_DIR = os.path.dirname(__file__)

class File:

    def __init__(self,id,file,current_user):
        self.id = id
        self.file = file
        self.current_user = current_user

    def __init__(self,file,current_user):
        self.id = uuid.uuid4()
        self.file = file
        self.current_user = current_user

    def __str__(self):
        return self.file.filename;

    def save(self):
        unique_file_id = uuid.uuid4()
        user_folder = os.path.join(BASE_DIR,'usersFiles',self.current_user.username,str(unique_file_id))

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        self.file.save(os.path.join(user_folder, self.file.filename))
