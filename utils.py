import re

class Utils:
    @staticmethod
    def sanitize_input(user_input):
        """Elimina caracteres no permitidos"""
        return re.sub(r'[^\w\s]', '', user_input)
