import requests

API_URL = "http://127.0.0.1:5000/jobs"

def generate_report():
    response = requests.get(API_URL)
    data = response.json()

    print(data)
    
    if response.status_code != 200:
        print("Erro ao obter vagas da API.")
        return
    
    jobs = response.json()

    report = {}

    for job in jobs:
        sector = job.get('sector', 'Indefinido')
        if sector not in report:
            report[sector] = []
        
        job_entry = {
            "title": job.get("title"),
            "code": job.get("code"),
            "description": job.get("description"),
            "salary": job.get("salary"),
            #"registration": job.get("registration") ou 
            #"matricula": job.get("matricula")
            "created_at": job.get("created_at"),
        }


        # Em um contexto original esse trecho não existiria pois se trata de um tratamento de excessão !
        # Mapeando o campo customizado "matricula"
        custom_fields = job.get("custom_fields", {})
        if "matricula" in custom_fields:
            job_entry["matricula"] = custom_fields["matricula"]
        
        # Incluindo outros campos customizados
        for key, value in custom_fields.items():
            if key not in job_entry:
                job_entry[key] = value

        report[sector].append(job_entry)
    
    # Salvando o relatório no arquivo sector_report.txt
    with open('sector_report.txt', 'w') as file:
        for sector, jobs in report.items():
            file.write(f"Setor: {sector}\n")
            for job in jobs:
                file.write(f"  Título: {job['title']}\n")
                file.write(f"  Código: {job['code']}\n")
                file.write(f"  Descrição: {job['description']}\n")
                file.write(f"  Salário: {job['salary']}\n")
                #file.write(f" Matrícula: {job['registration']}\n") ou
                #file.write(f" Registration: {job['registration']}\n")
                file.write(f"  Data de Criação: {job['created_at']}\n")
                if "matricula" in job:
                    file.write(f"  Matrícula: {job['matricula']}\n")
                # Escrever outros campos customizados que não foram mapeados anteriormente
                for key, value in job.items():
                    if key not in ["title", "code", "description", "salary", "created_at", "matricula"]:
                        file.write(f"  {key}: {value}\n")
                file.write("\n")

if __name__ == "__main__":
    generate_report()
