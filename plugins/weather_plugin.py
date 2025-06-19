name = 'weather_plugin'

def handle(text: str) -> str:
    """
    Exemplo de plugin que responde a frases relacionadas ao tempo.
    """
    if 'tempo' in text.lower() or 'previsão' in text.lower():
        # Aqui você poderia chamar uma API de clima real.
        return 'O tempo hoje está ensolarado com máxima de 25°C.'
    return ''