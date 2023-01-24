import uuid
import os


BASE_DIR = os.path.dirname(__file__)


def get_user_file_name(current_user, folderId):
    user_files_directory = os.path.join(BASE_DIR, 'usersFiles', current_user.username, str(folderId))
    return os.listdir(user_files_directory).pop()


def get_user_file_size(current_user, folderId):
    user_file_directory = os.path.join(BASE_DIR, 'usersFiles', current_user.username, str(folderId),get_user_file_name(current_user, folderId))
    return os.path.getsize(user_file_directory)

class File:

    def __init__(self, id, file, current_user):
        self.id = id
        self.file = file
        self.current_user = current_user

    def __init__(self, file, current_user):
        self.id = uuid.uuid4()
        self.file = file
        self.current_user = current_user

    def __str__(self):
        return self.file.filename;

    def save(self):
        unique_file_id = uuid.uuid4()
        user_folder = os.path.join(BASE_DIR, 'usersFiles', self.current_user.username, str(unique_file_id))

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        self.file.save(os.path.join(user_folder, self.file.filename))
    @staticmethod
    def show_user_files(current_user):

        user_files_directory = os.path.join(BASE_DIR,'usersFiles',current_user.username)

        if not os.path.exists(user_files_directory):
            os.makedirs(user_files_directory)

        files_folders = os.listdir(user_files_directory)

        return [dict({
            'filename': get_user_file_name(current_user,folderId),
            'folderId': folderId,
            'fileSize': get_user_file_size(current_user,folderId)
        }) for folderId in files_folders]

    @staticmethod
    def delete(current_user, folder_id):
        user_folder = os.path.join(BASE_DIR, 'usersFiles', current_user.username, folder_id)
        os.remove(os.path.join(user_folder, get_user_file_name(current_user,folder_id)))
        os.rmdir(user_folder)


