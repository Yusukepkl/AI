# Assistente Lia

Este repositório reúne diversos módulos que juntos implementam a **Lia**, uma assistente virtual simples. O projeto combina reconhecimento de fala, detecção de palavra-chave, entendimento de linguagem natural e uma interface gráfica em Qt.

## Requisitos

- Python 3.11
- Dependências listadas em `requirements.txt`
- Bibliotecas nativas para `pyaudio` e `simpleaudio`:
  ```bash
  sudo apt-get install portaudio19-dev libasound2-dev
  ```
- Principais bibliotecas Python:
  pvporcupine, webrtcvad, pyaudio, vosk,
  whispercpp, pyttsx3, simpleaudio, openai,
  googletrans, sqlalchemy, pyyaml, requests,
  kafka-python, paho-mqtt, PySide6,
  opentelemetry-api, opentelemetry-sdk,
  numpy

## Instalação

Antes de instalar as dependências Python, é necessário obter as bibliotecas nativas usadas por
`pyaudio` e `simpleaudio`:

```bash
sudo apt-get install portaudio19-dev libasound2-dev
```

Em seguida, instale os pacotes do projeto com:

```bash
pip install -r requirements.txt
```

Se preferir, execute `./setup.sh` para instalar automaticamente as dependências
nativas e os pacotes Python.

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
pv_access_key: "SUA-CHAVE-PORCUPINE"
pv_library_path: ""
pv_model_path: ""
pv_keyword_path: ""
pv_sensitivity: 0.5
audio_input_device: null
```

Use `audio_input_device` para especificar o índice do microfone quando existir
mais de um dispositivo conectado. Para descobrir os índices disponíveis:

```bash
python - <<'EOF'
import pyaudio, json
pa = pyaudio.PyAudio()
print(json.dumps({i: pa.get_device_info_by_index(i)["name"] for i in range(pa.get_device_count())}, indent=2))
EOF
```
Também é possível definir o dispositivo via variável de ambiente `AUDIO_INPUT_DEVICE`.

Para usar a detecção de hot-word Porcupine, obtenha uma chave gratuita em
[console.picovoice.ai](https://console.picovoice.ai/) e defina `pv_access_key`
no `config.yaml` ou a variável de ambiente `PV_ACCESS_KEY`.
Se desejar um modelo de palavra-chave personalizado, informe o caminho do
arquivo `.ppn` em `pv_keyword_path` (ou use a variável `PV_KEYWORD_PATH`).
Caso nenhum caminho seja fornecido, o modelo padrão "porcupine" será usado.
Se as bibliotecas do Porcupine estiverem fora do caminho padrão, defina também:
```bash
export PV_LIBRARY_PATH=/caminho/para/libpv_porcupine.so
export PV_MODEL_PATH=/caminho/para/porcupine_params.pv
export PV_SENSITIVITY=0.5
```
Esses valores podem ser configurados em `config.yaml`.


## Estrutura

Os módulos principais estão dentro do pacote `lia/` e incluem componentes de ASR, NLU, TTS, gestão de contexto, entre outros. Plugins personalizados podem ser adicionados em `lia/plugins`.

## Execução

1. Coloque um modelo do Vosk em `models/vosk-model-small`.
2. Inicie a interface Qt:

```bash
python main_ui.py
```

A janela da assistente será aberta e começará a escutar a palavra-chave configurada.
