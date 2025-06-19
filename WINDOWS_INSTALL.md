# Instalação passo a passo no Windows

Este guia descreve em detalhes como preparar o ambiente do projeto **Lia** em computadores com Windows.

## 1. Instalar o Python 3.11

1. Acesse [python.org](https://www.python.org/downloads/windows/).
2. Baixe o instalador da versão **Windows installer (64-bit)**.
3. Execute o instalador e marque a opção **Add python.exe to PATH** antes de clicar em *Install Now*.
4. Após a conclusão, abra o **Prompt de Comando** e verifique:
   ```cmd
   python --version
   ```
   O comando deve exibir `Python 3.11.x`.

## 2. Preparar o gerenciador de pacotes

Atualize o `pip` e instale o utilitário `pipwin`, que facilita a instalação de dependências que possuem binários pré-compilados:

```cmd
python -m pip install --upgrade pip
pip install pipwin
```

## 3. Instalar bibliotecas de áudio

Algumas dependências necessitam de módulos nativos. Use o `pipwin` para obtê-las já compiladas para Windows:

```cmd
pipwin install pyaudio
pip install simpleaudio
```

## 4. Obter o código do projeto

1. Clone este repositório ou baixe o arquivo ZIP disponível no GitHub.
2. Acesse a pasta do projeto no **Prompt de Comando**.

## 5. Instalar as dependências Python

Dentro da pasta do projeto, execute:

```cmd
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém todas as bibliotecas utilizadas, incluindo:

- reconhecimento e síntese de fala (`pvporcupine`, `webrtcvad`, `pyaudio`, `vosk`, `whispercpp`, `pyttsx3`, `simpleaudio`)
- integrações com APIs (`openai`, `googletrans`, `sqlalchemy`, `pyyaml`, `requests`)
- mensageria (`kafka-python`, `paho-mqtt`)
- interface gráfica (`PySide6`)
- telemetria (`opentelemetry-api`, `opentelemetry-sdk`)
- suporte numérico (`numpy`)

## 6. Executar a assistente

Após instalar as dependências, você já pode iniciar a interface da Lia:

```cmd
python main_ui.py
```

A janela da assistente será aberta e começará a escutar a palavra-chave definida em `config.yaml`.

Caso possua mais de um microfone conectado, consulte o README para descobrir os índices disponíveis e configure a opção `audio_input_device` no `config.yaml`.
