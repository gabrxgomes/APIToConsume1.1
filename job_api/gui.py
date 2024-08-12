import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

API_URL = "http://127.0.0.1:5000/jobs"

def submit_job():
    # Captura os valores dos campos
    title = title_entry.get()
    code = code_entry.get()
    description = description_entry.get("1.0", tk.END)
    salary = salary_entry.get()
    sector = sector_entry.get()
    
    # Verifica se todos os campos obrigatórios foram preenchidos
    if not title or not code or not description.strip() or not salary or not sector:
        messagebox.showwarning("Campos obrigatórios", "Por favor, preencha todos os campos obrigatórios.")
        return

    # Dados da vaga em formato JSON
    job_data = {
        "title": title,
        "code": code,
        "description": description.strip(),
        "salary": float(salary),
        "sector": sector
    }

    # Adicionar parâmetros customizados dinamicamente
    while True:
        add_param = messagebox.askyesno("Adicionar Parâmetro", "Deseja adicionar um parâmetro customizável?")
        if not add_param:
            break
        param_name = simpledialog.askstring("Nome do Parâmetro", "Digite o nome do parâmetro:")
        param_value = simpledialog.askstring("Valor do Parâmetro", "Digite o valor do parâmetro:")
        
        if param_name and param_value:
            job_data[param_name] = param_value # Envia o valor puxado das labels para a lista job_data
        else:
            messagebox.showwarning("Parâmetro inválido", "Nome e valor do parâmetro não podem ser vazios.")

    # Envia os dados para a API, como parametros passamos a API_URL e fazemos a variavel "json" receber os dados das labels no arquivo "jobs.json"
    response = requests.post(API_URL, json=job_data)

    if response.status_code == 201:
        messagebox.showinfo("Sucesso", "Vaga criada com sucesso!")
    else:
        messagebox.showerror("Erro", f"Falha ao criar a vaga. Código de status: {response.status_code}")

# Configuração da janela principal
root = tk.Tk()
root.title("Adicionar Nova Vaga")

# Labels e entradas de texto
tk.Label(root, text="Título da Vaga").grid(row=0, column=0, padx=10, pady=10)
title_entry = tk.Entry(root, width=40)
title_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Código da Vaga").grid(row=1, column=0, padx=10, pady=10)
code_entry = tk.Entry(root, width=40)
code_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Descrição da Vaga").grid(row=2, column=0, padx=10, pady=10)
description_entry = tk.Text(root, width=40, height=5)
description_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Salário da Vaga").grid(row=3, column=0, padx=10, pady=10)
salary_entry = tk.Entry(root, width=40)
salary_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Setor da Vaga").grid(row=4, column=0, padx=10, pady=10)
sector_entry = tk.Entry(root, width=40)
sector_entry.grid(row=4, column=1, padx=10, pady=10)

# Botão de submissão
submit_button = tk.Button(root, text="Adicionar Vaga", command=submit_job)
submit_button.grid(row=5, column=1, pady=20)

# Inicia a interface gráfica
root.mainloop()
