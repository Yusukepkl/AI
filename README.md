# Assistente Lia

Este repositório reúne diversos módulos que juntos implementam a **Lia**, uma assistente virtual simples. O projeto combina reconhecimento de fala, detecção de palavra-chave, entendimento de linguagem natural e uma interface gráfica em Qt.

## Requisitos

- Python 3.11
- Dependências listadas em `requirements.txt`
- Bibliotecas nativas para `pyaudio` e `simpleaudio`:
  ```bash
  sudo apt-get install portaudio19-dev libasound2-dev
  ```

## Instalação

Instale os pacotes do projeto com:

```bash
pip install -r requirements.txt
```

## Configuração

Todas as opções de execução são lidas de `config.yaml`. Um exemplo é mostrado abaixo:

```yaml
openai_api_key: "SUA-CHAVE-OPENAI"
vad_mode: 1
kafka_broker: "localhost:9092"
db_url: "sqlite:///lia_context.db"
ws_host: "0.0.0.0"
ws_port: 8765
auth_token: "token123"
languages: ["pt", "en", "es"]
mqtt_broker: "localhost"
vosk_model_path: "models/vosk-model-small"
whisper_model: "small"
rasa_url: "http://localhost:5005/model/parse"
```

## Estrutura

Os módulos principais estão dentro do pacote `lia/` e incluem componentes de ASR, NLU, TTS, gestão de contexto, entre outros. Plugins personalizados podem ser adicionados em `lia/plugins`.

## Execução

1. Coloque um modelo do Vosk em `models/vosk-model-small`.
2. Inicie a interface Qt:

```bash
python main_ui.py
```

A janela da assistente será aberta e começará a escutar a palavra-chave configurada.
