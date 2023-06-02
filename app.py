from flask import Flask, request, jsonify, send_file
from crawler import Crawler

app = Flask(__name__)

@app.route('/crawler_linkedin', methods=['POST'])
def crawler_linkedin():
    
    # Check if the CSV file was sent in the request
    if 'companies_file' not in request.files:
        return jsonify({'error': 'No files uploaded'})

    companies_file = request.files['companies_file']

    # Check if the file has a CSV extension
    if not companies_file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be of type CSV'})

    linkedin_urls_file_name = 'linkedin_urls.csv'
    #Read the CSV file
    try:
        crawler = Crawler()

        crawler.get_linkedin_urls(companies_file, linkedin_urls_file_name)

        linkedin_urls_file = open(linkedin_urls_file_name)

        crawler.update_employee_count(companies_file, linkedin_urls_file)

    except Exception as e:
        return jsonify({'error': f'Error reading CSV file: {str(e)}'})
    

    # Retornar o arquivo CSV de saída
    return send_file(companies_file.name, as_attachment=True)

if __name__ == '__main__':
    app.run()
