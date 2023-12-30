import tkinter as tk
from tkinter import filedialog, ttk
import os
import shutil
import csv
from tkinter import messagebox

arquivo_selecionado = ""
colunas = []


def selecionar_pasta_origem():
    pasta_origem = filedialog.askdirectory()
    entry_origem.delete(0, tk.END)
    entry_origem.insert(0, pasta_origem)
    verificar_campos()


def selecionar_pasta_destino():
    pasta_destino = filedialog.askdirectory()
    entry_destino.delete(0, tk.END)
    entry_destino.insert(0, pasta_destino)
    verificar_campos()


def verificar_campos():
    if entry_origem.get() and entry_destino.get() and combobox_colunas.get():
        botao_mover['state'] = tk.NORMAL
    else:
        botao_mover['state'] = tk.DISABLED
    if entry_origem.get():
        botao_selecionar_arquivo['state'] = tk.NORMAL
    else:
        botao_selecionar_arquivo['state'] = tk.DISABLED


def selecionar_arquivo():
    global arquivo_selecionado, colunas
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    entry_arquivo.delete(0, tk.END)
    entry_arquivo.insert(0, arquivo)
    arquivo_selecionado = arquivo

    combobox_colunas['values'] = ()
    colunas = []
    if arquivo:
        mostrar_colunas(arquivo)


def mostrar_colunas(arquivo):
    global colunas
    try:
        with open(arquivo, 'r') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)
            colunas = header
            print("Colunas encontradas:")
            combobox_colunas['values'] = colunas
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")


def verificar_existencia_arquivo(origem, arquivo):
    caminho_arquivo = os.path.join(origem, f"{arquivo}.xml")
    return os.path.exists(caminho_arquivo)


def mostrar_dados_coluna(coluna_selecionada):
    origem = entry_origem.get()
    arquivo = os.path.join(origem, arquivo_selecionado)
    if os.path.exists(arquivo):
        try:
            with open(arquivo, 'r') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                indice_coluna = header.index(coluna_selecionada) if coluna_selecionada in header else None
                if indice_coluna is not None:
                    dados_coluna = [row[indice_coluna] for row in reader]
                    print(f"Dados da coluna '{coluna_selecionada}':")
                    print(dados_coluna)

                    tree.delete(*tree.get_children())

                    for dado in dados_coluna:
                        arquivo_existe = verificar_existencia_arquivo(origem, dado)
                        tree.insert("", tk.END, values=(dado, "Sim" if arquivo_existe else "Não"))

                    verificar_campos()
                else:
                    print(f"Coluna '{coluna_selecionada}' não encontrada no arquivo.")
        except Exception as e:
            print(f"Erro ao exibir os dados da coluna: {e}")


def mover_arquivos():
    origem = entry_origem.get()
    destino = entry_destino.get()

    for item in tree.get_children():
        dado = tree.item(item)['values'][0]
        arquivo_existe = tree.item(item)['values'][1]

        origem_arquivo = os.path.join(origem, f"{dado}.xml")
        destino_arquivo = os.path.join(destino, f"{dado}.xml")
        if arquivo_existe == "Sim" and os.path.exists(origem_arquivo):
            shutil.move(origem_arquivo, destino_arquivo)
            print(f"Arquivo '{dado}' movido para '{destino}'.")
    messagebox.showinfo("Arquivos Movidos", "Os arquivos foram movidos com sucesso para o destino selecionado.")


root = tk.Tk()
root.title("Selecionar Arquivo CSV e Destino")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_origem = tk.Label(frame, text="Pasta de Origem:")
label_origem.grid(row=0, column=0, padx=5, pady=5)

entry_origem = tk.Entry(frame, width=30)
entry_origem.grid(row=0, column=1, padx=5, pady=5)

botao_selecionar_origem = tk.Button(frame, text="Selecionar Origem", command=selecionar_pasta_origem)
botao_selecionar_origem.grid(row=0, column=2, padx=5, pady=5)

label_destino = tk.Label(frame, text="Pasta de Destino:")
label_destino.grid(row=1, column=0, padx=5, pady=5)

entry_destino = tk.Entry(frame, width=30)
entry_destino.grid(row=1, column=1, padx=5, pady=5)

botao_selecionar_destino = tk.Button(frame, text="Selecionar Destino", command=selecionar_pasta_destino)
botao_selecionar_destino.grid(row=1, column=2, padx=5, pady=5)

label_arquivo = tk.Label(frame, text="Arquivo CSV:")
label_arquivo.grid(row=2, column=0, padx=5, pady=5)

entry_arquivo = tk.Entry(frame, width=30)
entry_arquivo.grid(row=2, column=1, padx=5, pady=5)

botao_selecionar_arquivo = tk.Button(frame, text="Selecionar Arquivo", command=selecionar_arquivo, state=tk.DISABLED)
botao_selecionar_arquivo.grid(row=2, column=2, padx=5, pady=5)
label_colunas = tk.Label(frame, text="Colunas:")
label_colunas.grid(row=3, column=0, padx=5, pady=5)

combobox_colunas = ttk.Combobox(frame, state="readonly", width=27)
combobox_colunas.grid(row=3, column=1, padx=5, pady=5)
combobox_colunas.bind("<<ComboboxSelected>>", lambda event: mostrar_dados_coluna(combobox_colunas.get()))
tree = ttk.Treeview(frame, columns=("Dado", "Arquivo Existe"), show="headings")
tree.heading("#1", text="Dado")
tree.heading("#2", text="Arquivo Existe")
tree.column("#1", width=200, anchor=tk.CENTER, stretch=tk.YES)
tree.column("#2", width=100, anchor=tk.CENTER, stretch=tk.YES)
tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
botao_mover = tk.Button(frame, text="Mover Arquivos", command=mover_arquivos,
                        state=tk.DISABLED)
botao_mover.grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
