#!/usr/bin/env bash
set -e

# Instala dependências de áudio necessárias para pyaudio e simpleaudio
sudo apt-get update
sudo apt-get install -y portaudio19-dev libasound2-dev

# Instala pacotes Python
pip install -r requirements.txt
