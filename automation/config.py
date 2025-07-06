import os
from dotenv import load_dotenv

load_dotenv()  # carrega as variáveis do .env para o ambiente

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'leticiabedoni'
REPO_NAME = 'github-issues-report'
USUARIOS_DE_INTERESSE = ['leticiabedoni']

