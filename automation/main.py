import requests
import pandas as pd
from automation.config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME, USUARIOS_DE_INTERESSE

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

def coletar_issues():
    issues_data = []
    page = 1

    while True:
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues'
        params = {'state': 'closed', 'per_page': 100, 'page': page}
        response = requests.get(url, headers=headers, params=params)
        issues = response.json()

        if not issues:
            break

        for issue in issues:
            if 'pull_request' in issue:
                continue

            autor = issue['user']['login']
            if autor not in USUARIOS_DE_INTERESSE:
                continue

            timeline_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue['number']}/timeline"
            timeline_resp = requests.get(timeline_url, headers={
                **headers,
                'Accept': 'application/vnd.github.mockingbird-preview+json'
            })
            timeline = timeline_resp.json()

            closed_by = 'desconhecido'
            for event in timeline:
                if event.get('event') == 'closed' and event.get('actor'):
                    closed_by = event['actor']['login']
                    break

            issues_data.append({
                'Número': issue['number'],
                'Aberta em': issue['created_at'],
                'Fechada em': issue['closed_at'],
                'Quem Abriu': autor,
                'Quem Fechou': closed_by
            })

        page += 1

    return issues_data

def main():
    issues = coletar_issues()
    if not issues:
        print("Nenhuma issue encontrada para os usuários filtrados.")
        return

    df = pd.DataFrame(issues)
    df.to_excel('data/relatorio_issues.xlsx', index=False)
    print("Relatório gerado com sucesso: data/relatorio_issues.xlsx")

if __name__ == '__main__':
    main()
