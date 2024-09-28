import bcrypt


class Security:

    @staticmethod
    def set_password(raw_password) -> str:
        return str(bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()))

    @staticmethod
    def check_password(raw_password, enc_password) -> bool:
        return bcrypt.checkpw(raw_password.encode("utf-8"), enc_password)
