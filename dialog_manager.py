from config import config


class DialogManager:
    def __init__(self):
        self.context = []

    def get_msgs(self, user_text: str) -> list:
        # guarda a mensagem do usuário e retorna as últimas N trocas
        self.context.append({"role": "user", "content": user_text})
        return self.context[-config.LANGUAGES.__len__() :]
