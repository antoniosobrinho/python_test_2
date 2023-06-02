from flask import Flask, request, jsonify, send_file
from scrapy import Scrapy

app = Flask(__name__)

@app.route('/process_csv', methods=['POST'])
def process_csv():
    # Verificar se o arquivo CSV foi enviado na requisição
    if 'companies_file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'})

    companies_file = request.files['companies_file']

    # Verificar se o arquivo tem uma extensão CSV
    if not companies_file.filename.endswith('.csv'):
        return jsonify({'error': 'Arquivo deve ser do tipo CSV'})

    output_file_name = 'output_file.csv'
    # Ler o arquivo CSV
    try:
        scrapy = Scrapy()

        scrapy.find_linkedin_urls(companies_file, output_file_name)

        output_file = open(output_file_name)

        scrapy.update_employee_count(companies_file, output_file)
    except Exception as e:
        return jsonify({'error': f'Erro ao ler o arquivo CSV: {str(e)}'})
    

    # Retornar o arquivo CSV de saída
    return send_file(output_file.name, as_attachment=True)

if __name__ == '__main__':
    app.run()
