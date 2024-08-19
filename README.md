## Apresentação

```markdown
# PDF Converter Script

Este script converte arquivos PDF em arquivos Excel, CSV e DOCX. Ele usa as bibliotecas `pdfplumber`, `pandas`, `openpyxl` e `python-docx` para extrair tabelas de PDFs e gerar arquivos nos formatos mencionados.

## Requisitos

Certifique-se de ter o Python 3.9 instalado em seu sistema.
```

### 1. Clone o repositório ou baixe o script

```bash
git clone https://github.com/Tommendes/pdfConverter.git 
cd pdfConverter
```

### 2. Crie e ative um ambiente virtual Python

```bash
python3.9 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### Dependências

As bibliotecas necessárias estão listadas no arquivo `requirements.txt`:

- pdfplumber
- pandas
- openpyxl
- python-docx

### 4. Execução do Script

Para executar o script, basta rodar o comando abaixo, passando o arquivo PDF que deseja converter:

```bash
python pdfConverter.py <nome_do_arquivo.pdf>
```

Os arquivos de saída serão gerados com o mesmo nome base que o PDF, nos formatos Excel, CSV e DOCX.

## Exemplo

```bash
python pdfConverter.py TO0316082024-ATIVOS.pdf
```

## Automação da Instalação

Se preferir, você pode executar o script abaixo para automatizar a instalação e ativação do ambiente virtual:

```bash
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
```

Para usar este script, você pode rodar:

```bash
bash setup.sh
```

O `setup.sh` irá configurar tudo automaticamente para você. Depois disso, você pode executar o script como explicado anteriormente.

---

### Notas

- Certifique-se de que o Python 3.9 está instalado.
- Siga os passos de instalação cuidadosamente.
- O script espera que o PDF contenha tabelas que possam ser extraídas. Verifique a qualidade do PDF caso o resultado esteja inconsistente.