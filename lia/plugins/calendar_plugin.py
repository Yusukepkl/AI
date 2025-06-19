name = "calendar_plugin"


def handle(text: str) -> str:
    """
    Exemplo de plugin que responde a agendamentos simples.
    """
    if "agendar" in text.lower() and "reunião" in text.lower():
        return "Claro, em que data você gostaria de agendar a reunião?"
    return ""
