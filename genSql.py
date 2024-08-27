import csv
import sys
import hashlib
from datetime import datetime, timedelta

def calculate_primeiro_vencimento(parcela):
    # Mês atual é agosto de 2024
    current_month = 8
    current_year = 2024
    num_parcela = int(parcela.split('/')[0])
    primeiro_vencimento_date = datetime(current_year, current_month, 1) - timedelta(days=(num_parcela - 1) * 30)
    return primeiro_vencimento_date.strftime('%Y-%m-%d')

def convert_pt_br_to_float(value):
    # Remove os pontos e substitui a vírgula por ponto
    return float(value.replace('.', '').replace(',', '.'))

def convert_pt_br_date_to_iso(date_str):
    # Converte a data do formato DD/MM/YYYY para YYYY-MM-DD
    return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')

def generate_sql_from_csv(csv_file_path):
    values_list = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            cpf = row['CPF']
            contrato = row['Contrato']
            parcela = row['Parcela']
            valor_parcela = convert_pt_br_to_float(row['Valor da Parcela'])
            dt_contrato = convert_pt_br_date_to_iso(row['Dt. Contrato'])

            primeiro_vencimento = calculate_primeiro_vencimento(parcela)
            parcelas = int(parcela.split('/')[1])
            valor_total = valor_parcela * parcelas
            valor_liquido = valor_total
            token = hashlib.sha256(contrato.encode()).hexdigest()

            values = f"""
                (NULL, 10, 1, NOW(), NULL, '{token}', 562, 1,
                (SELECT cs.id FROM cad_servidores cs JOIN fin_sfuncional ff ON ff.id_cad_servidores = cs.id WHERE cpf = '{cpf}' AND ff.situacao = 1 AND (ff.mes = '07' OR ff.mes = '08') AND ff.ano = '2024' GROUP BY cs.id ORDER BY CAST(ff.mes AS UNSIGNED) LIMIT 1),
                NULL, '{contrato}', '{primeiro_vencimento}', {valor_parcela:.2f}, {parcela.split('/')[0]}, {parcelas}, {valor_total:.2f}, {valor_liquido:.2f}, 0, 0, '{dt_contrato}', NULL)
            """
            values_list.append(values.strip())

    sql = f"""
    INSERT INTO con_contratos (
        id, STATUS, evento, created_at, updated_at, token, id_user, id_consignatario, id_cad_servidores, id_con_eventos, contrato, primeiro_vencimento, valor_parcela, parcela, parcelas, valor_total, valor_liquido, qmar, averbado_online, data_averbacao, data_liquidacao
    ) VALUES
    {', '.join(values_list)};
    """

    with open('genSql.sql', 'w', encoding='utf-8') as sqlfile:
        sqlfile.write(sql.strip())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python genSql.py <arquivo_csv>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    generate_sql_from_csv(csv_file_path)
    print("Arquivo SQL gerado: genSql.sql")