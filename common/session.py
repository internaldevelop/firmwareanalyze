

class UserSession:
    l_user_uuid = ''
    l_user_account = ''
    l_user_name = ''

    @staticmethod
    def set_user(uuid, account, name):
        if uuid is not None:
            UserSession.l_user_uuid = uuid
        if account is not None:
            UserSession.l_user_account = account
        if name is not None:
            UserSession.l_user_name = name
        return

    @staticmethod
    def get_user():
        return UserSession.l_user_uuid, UserSession.l_user_account, UserSession.l_user_name

    @staticmethod
    def get_uuid():
        return UserSession.l_user_uuid

    @staticmethod
    def get_account():
        return UserSession.l_user_account

    @staticmethod
    def get_name():
        return UserSession.l_user_name
