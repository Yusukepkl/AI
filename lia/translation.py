# translation.py
from googletrans import Translator

translator = Translator()


def translate(text: str, dest: str = "en") -> str:
    """
    Detecta o idioma de `text` e, se for diferente de `dest`, faz a tradução.
    """
    # PyCharm vê detect() como coroutine, mas a implementação é síncrona
    detected = translator.detect(text)  # type: ignore
    lang = detected.lang  # type: ignore

    if lang != dest:
        result = translator.translate(text, dest=dest)  # type: ignore
        return result.text  # type: ignore

    return text
