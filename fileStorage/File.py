import uuid
import os

from fileStorage import app
from fileStorage.utils import convert_bytes

BASE_DIR = os.path.join(os.path.dirname(__file__),app.config["UPLOAD_FOLDER"])

class File:

    def __init__(self, file, current_user):
        self.folder_id = uuid.uuid4()
        self.file = file
        self.current_user = current_user

    def __str__(self):
        return self.file.filename

    def get_folder_id(self):
        return str(self.folder_id)

    def save(self):
        unique_file_id = self.folder_id
        user_folder = os.path.join(BASE_DIR, self.current_user.username, str(unique_file_id))

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        self.file.save(os.path.join(user_folder, self.file.filename))

    @classmethod
    def get_user_file_name(cls, current_user, folderId):
        user_files_directory = os.path.join(BASE_DIR, current_user.username, str(folderId))
        return os.listdir(user_files_directory).pop()

    @classmethod
    def get_user_file_size(cls, current_user, folderId):
        user_file_directory = os.path.join(BASE_DIR, current_user.username, str(folderId),
                                           File.get_user_file_name(current_user, folderId))
        return os.path.getsize(user_file_directory)

    @classmethod
    def get_file_directory(cls, current_user, folderId):
        file_directory = os.path.join(BASE_DIR, current_user.username, str(folderId))
        return file_directory

    @classmethod
    def get_file(cls, current_user, folderId):
        file = os.path.join(BASE_DIR, current_user.username, str(folderId), File.get_user_file_name(current_user, folderId))
        return file

    @staticmethod
    def show_user_files(current_user):

        user_files_directory = os.path.join(BASE_DIR,current_user.username)

        if not os.path.exists(user_files_directory):
            os.makedirs(user_files_directory)

        files_folders = os.listdir(user_files_directory)

        return [dict({
            'filename': File.get_user_file_name(current_user,folderId),
            'folderId': folderId,
            'fileSize': convert_bytes(File.get_user_file_size(current_user,folderId))
        }) for folderId in files_folders]

    @staticmethod
    def delete(current_user, folder_id):
        user_folder = os.path.join(BASE_DIR, current_user.username, folder_id)
        os.remove(os.path.join(user_folder, File.get_user_file_name(current_user,folder_id)))
        os.rmdir(user_folder)


