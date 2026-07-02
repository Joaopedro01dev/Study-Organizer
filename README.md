# Backend Template

Backend Flask simples para servir como base no hackathon.

## Requisitos

- Python 3.11+
- `pip`

## Instalação

Crie e ative um ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

## Variáveis de ambiente

Crie um arquivo `.env` com base em `.env.example`

## Banco de dados

O projeto usa SQLite por padrão e grava o banco em `app.db`.

Aplicar as migrations existentes:

```powershell
python -m flask --app main db upgrade
```

Criar uma nova migration apos alterar os models:

```powershell
flask --app main db migrate -m "describe your change"
flask --app main db upgrade
```

## Popular banco com usuário admin

O script abaixo cria ou atualiza um usuário administrador inicial.

Valores padrão:

- `ADMIN_EMAIL=admin@hackathon.local`
- `ADMIN_PASSWORD=admin123`

Voce pode sobrescrever esses valores definindo as variáveis de ambiente `ADMIN_EMAIL` e `ADMIN_PASSWORD`. Para executar:

```powershell
python populate_database.py
```

## Executando a aplicação

Modo desenvolvimento:

```powershell
python main.py
```

A aplicação sobe em `http://localhost:5000` e a documentação da API fica em `http://localhost:5000/docs`.
