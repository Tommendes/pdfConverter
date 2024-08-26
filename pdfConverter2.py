import re
import pdfplumber
import os
import sys

def split_line_by_patterns(line):
    """
    Divide a linha de texto com base em padrões como CPF, número de contrato, datas e valores,
    inserindo delimitadores onde apropriado.
    """
    # Define padrões para CPF (11 dígitos seguidos), contratos (9 dígitos seguidos), datas e valores
    cpf_pattern = r'(\d{11})'
    contract_pattern = r'(\d{9})'
    date_pattern = r'(\d{2}/\d{2}/\d{4})'
    value_pattern = r'(\d{1,3}(?:\.\d{3})*,\d{2})'

    # Substituir esses padrões por eles mesmos com delimitadores (;)
    line = re.sub(cpf_pattern, r';\1;', line)
    line = re.sub(contract_pattern, r';\1;', line)
    line = re.sub(date_pattern, r';\1;', line)
    line = re.sub(value_pattern, r';\1;', line)

    # Remover possíveis delimitadores duplicados
    line = re.sub(r';{2,}', ';', line).strip(';')

    return line

def convert_pdf_to_csv_with_delimiters(pdf_path):
    # Definir o caminho de saída
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    csv_path = f"{base_name}_processed.csv"

    # Abrir o arquivo PDF
    with pdfplumber.open(pdf_path) as pdf:
        extracted_text = ''
        for page in pdf.pages:
            # Extraindo todo o texto da página
            extracted_text += page.extract_text()

    # Processamento do texto para adicionar delimitadores adequados com base nos padrões
    if extracted_text:
        processed_lines = []
        for line in extracted_text.split('\n'):
            # Processar cada linha para melhorar a separação por colunas
            processed_line = split_line_by_patterns(line)
            processed_lines.append(processed_line)

        # Escrever o texto processado em CSV
        with open(csv_path, 'w') as file:
            file.write('\n'.join(processed_lines))

    return csv_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python pdfConverter2.py <arquivo_pdf>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    if not os.path.isfile(pdf_file):
        print(f"Arquivo não encontrado: {pdf_file}")
        sys.exit(1)

    # Chamar a função de conversão
    csv_output_path = convert_pdf_to_csv_with_delimiters(pdf_file)
    print(f"Arquivo CSV gerado: {csv_output_path}")