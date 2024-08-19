#!/bin/bash

# Verificar se o Python 3.9 está instalado
if ! command -v python3.9 &> /dev/null
then
    echo "Python 3.9 não encontrado. Instale o Python 3.9 antes de continuar."
    exit
fi

# Criar o ambiente virtual
python3.9 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar as dependências
pip install -r requirements.txt

echo "Ambiente virtual configurado e dependências instaladas."