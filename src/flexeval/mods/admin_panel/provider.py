from flexeval.core.providers.auth import AuthProvider, User


class AdminUser(User):
    __tablename__ = "AdminUser"

    def __init__(self):
        super().__init__()


class AdminAuthProvider(AuthProvider):
    def connect(self):
        super()._connect(AdminUser())
