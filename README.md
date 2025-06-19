# Lia AI Assistant

This repository contains a collection of modules that together implement a simple AI assistant called **Lia**.  The project mixes speech recognition, hotword detection, natural language understanding and a Qt based user interface.

## Requirements

Python 3.11 is recommended.  The dependencies can be installed with:

```bash
pip install -r requirements.txt
```

Some optional packages such as `rasa` are not available for Python 3.11.  The basic features work without them.

## Configuration

All runtime options are read from `config.yaml`.  A sample configuration is provided below:

```yaml
openai_api_key: "YOUR-OPENAI-KEY"
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

## Running

1. Ensure a Vosk model is placed inside `models/vosk-model-small`.
2. Run the Qt interface:

```bash
python main_ui.py
```

The assistant window will open and start listening for the hotword defined via Porcupine.
