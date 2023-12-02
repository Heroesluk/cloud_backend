from datetime import datetime


class User:
    def __init__(self, id: int, username: str, password: str, email: str):
        self.id = id
        self.username = username
        self.password = password
        self.email = email


class Image:
    def __init__(self, id, name: str, folder_id: int, image_size: int, image_add_date: datetime):
        self.image_add_date = image_add_date
        self.image_size = image_size
        self.folder_id = folder_id
        self.id = id
        self.name = name
        self.signed_url = None

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'folder_id': self.folder_id,
            'image_size': self.image_size,
            'image_add_date': self.image_add_date,
            'url': self.signed_url
        }

    def get_bucket_path(self):
        return str(self.folder_id) + "/" + self.name
