#!/bin/bash

# Remove o venv antigo se existir
rm -rf venv

# Verifica se Python 3.11 está instalado, senão usa python3 padrão
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
    echo "Usando Python 3.11"
else
    PYTHON_CMD=python3
    echo "Python 3.11 não encontrado, usando python3 padrão"
    echo "analisar a possibilidade de instalar o Python 3.11"
    echo "brew install python@3.11"
fi

# Cria um novo ambiente virtual com a versão especificada
$PYTHON_CMD -m venv venv

# Ativa o ambiente virtual
source ./venv/bin/activate

# Mostra a versão do Python sendo usada
python --version

# Atualiza o pip
pip install --upgrade pip

# Instala a versão mais recente do chromadb
#pip install --upgrade chromadb
pip install chromadb==1.3.5

pip show chromadb