# CSV Column Shifter

O "CSV Column Shifter" é uma ferramenta simples em Python que permite selecionar arquivos CSV, visualizar suas colunas e mover os arquivos correspondentes para uma pasta de destino.

## Requisitos

Certifique-se de ter Python 3 instalado no seu sistema.

Você pode instalar as dependências necessárias executando:

```bash
pip install -r requirements.txt
```

## Como Usar
-  Execute o programa Python:
```bash
python index.py
```
- Selecione a pasta de origem e destino.
- Selecione o arquivo CSV.
- Selecione a coluna desejada para visualização.
- Após selecionar a coluna, a tabela será preenchida.
- Clique em "Mover Arquivos" para mover os arquivos correspondentes para a pasta de destino.

## Dependências
- tkinter: Biblioteca para criar interfaces gráficas.
- os: Manipulação de caminhos de arquivos.
- shutil: Mover arquivos.
- csv: Leitura de arquivos CSV.
- messagebox (de tkinter): Exibir caixas de mensagem.

## Compilação
```bash
  pyinstaller --onefile index.py
```

## Contribuição
Contribuições são bem-vindas!

Abra um Pull Request ou crie uma Issue para discutir novos recursos ou correções.

## Licença
Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.