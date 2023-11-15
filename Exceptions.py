
class UserTableDuplicateUsername(Exception):
    def __init__(self, username):
        self.message = f"There's duplicate username in Users table: {username}"
        super().__init__(self.message)
