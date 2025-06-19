# AGENTS

Todas as instruções a seguir se aplicam a todo o repositório.

- Utilize **Python 3.11**.
- Antes de commitar rode os seguintes passos:

```bash
pip install -r requirements.txt
pip install black ruff pytest
black . --line-length 120
ruff .
pytest -q
```

- Indente o código com 4 espaços e siga PEP8.
- Adicione anotações de tipo sempre que possível.
- Escreva mensagens de commit breves no imperativo (ex: "Adiciona teste").
