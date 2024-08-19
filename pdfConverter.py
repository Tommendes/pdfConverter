import pdfplumber
import pandas as pd
from docx import Document
from openpyxl import load_workbook
from openpyxl.styles import NamedStyle
from openpyxl.utils.dataframe import dataframe_to_rows
import sys
import os

def convert_pdf_to_formats(pdf_path):
    # Definir os caminhos dos arquivos de saída
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    excel_path = f"{base_name}.xlsx"
    csv_path = f"{base_name}.csv"
    docx_path = f"{base_name}.docx"

    # Abrir o arquivo PDF
    with pdfplumber.open(pdf_path) as pdf:
        tables = []
        # Iterar pelas páginas do PDF
        for page in pdf.pages:
            # Extrair a tabela de cada página
            table = page.extract_table()
            if table:
                tables.extend(table)

    # Converter os dados extraídos para DataFrame
    df = pd.DataFrame(tables[1:], columns=tables[0])  # Adiciona cabeçalhos se presentes

    # Salvar o DataFrame como um arquivo CSV
    df.to_csv(csv_path, index=False)

    # Salvar o DataFrame como um arquivo DOCX
    doc = Document()
    if not df.empty:
        table = doc.add_table(rows=1, cols=len(df.columns))
        
        # Adicionar cabeçalhos
        hdr_cells = table.rows[0].cells
        for i, column in enumerate(df.columns):
            hdr_cells[i].text = column

        # Adicionar dados
        for index, row in df.iterrows():
            row_cells = table.add_row().cells
            for i, value in enumerate(row):
                row_cells[i].text = str(value)
        
        doc.save(docx_path)
    else:
        print("DataFrame vazio. Nenhum arquivo DOCX gerado.")

    # Salvar o DataFrame como um arquivo Excel
    df.to_excel(excel_path, index=False)

    # Formatar o arquivo Excel
    wb = load_workbook(excel_path)
    ws = wb.active

    # Definir um estilo de formatação para valores monetários
    currency_style = NamedStyle(name='currency_style', number_format='$#,##0.00')

    # Aplicar o estilo a uma coluna específica (por exemplo, a terceira coluna, índice 2)
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=3, max_row=ws.max_row):
        for cell in row:
            cell.style = currency_style

    # Salvar o arquivo Excel com a formatação
    wb.save(excel_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python pdfConverter.py <arquivo_pdf>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    if not os.path.isfile(pdf_file):
        print(f"Arquivo não encontrado: {pdf_file}")
        sys.exit(1)

    # Chamar a função de conversão
    convert_pdf_to_formats(pdf_file)
