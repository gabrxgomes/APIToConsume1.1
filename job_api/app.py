from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = 'data/jobs.json'

def read_jobs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def write_jobs(jobs):
    with open(DATA_FILE, 'w') as file:
        json.dump(jobs, file, indent=4)

@app.route('/jobs', methods=['POST'])
def create_job():
    job_data = request.json
    
    title = job_data.get('title')
    code = job_data.get('code')
    description = job_data.get('description')
    salary = job_data.get('salary')
    sector = job_data.get('sector')
    
    if not title or not code or not description or not salary or not sector:
        return jsonify({"error": "Todos os campos obrigatórios devem ser preenchidos"}), 400

    # Criação da vaga com os dados fornecidos
    job = {
        "title": title,
        "code": code,
        "description": description,
        "salary": salary,
        "sector": sector,
        "created_at": datetime.now().isoformat(),
        "custom_fields": {}
    }
    
    for key, value in job_data.items():
        if key not in ["title", "code", "description", "salary", "sector"]:
            job["custom_fields"][key] = value

    # Armazenar a vaga no arquivo JSON
    jobs = read_jobs()
    jobs.append(job)
    write_jobs(jobs)
    
    return jsonify({"message": "Vaga criada com sucesso!"}), 201

@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = read_jobs()
    return jsonify(jobs), 200

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)  # Garante que a pasta data exista
    app.run(debug=True)
