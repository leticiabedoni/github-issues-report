import boto3
from automation.github_collector import coletar_issues, gerar_excel

# Configuração SES
ses_client = boto3.client("ses", region_name="us-east-1")

REMETENTE = "leticiabedoni@hotmail.com"
DESTINATARIO = "leticiabedoni@hotmail.com"
ASSUNTO = "📊 Relatório de issues fechadas"
CORPO_EMAIL = """
Olá!

Segue em anexo o relatório de issues fechadas dos últimos 30 dias no repositório monitorado.

Atenciosamente,  
Bot GitHub Lambda 🤖
"""

def criar_email_raw(destinatario, assunto, corpo, arquivo_bytes, nome_arquivo):
    import email.mime.multipart
    import email.mime.text
    import email.mime.application

    msg = email.mime.multipart.MIMEMultipart()
    msg["Subject"] = assunto
    msg["From"] = REMETENTE
    msg["To"] = destinatario

    msg.attach(email.mime.text.MIMEText(corpo))

    part = email.mime.application.MIMEApplication(arquivo_bytes)
    part.add_header("Content-Disposition", "attachment", filename=nome_arquivo)
    msg.attach(part)

    return msg.as_string()

def lambda_handler(event, context):
    try:
        issues = coletar_issues()
        excel_bytes = gerar_excel(issues)
        email_raw = criar_email_raw(DESTINATARIO, ASSUNTO, CORPO_EMAIL, excel_bytes, "relatorio_issues.xlsx")

        response = ses_client.send_raw_email(
            Source=REMETENTE,
            Destinations=[DESTINATARIO],
            RawMessage={"Data": email_raw}
        )

        return {
            "statusCode": 200,
            "body": f"E-mail enviado com sucesso! ID: {response['MessageId']}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Erro ao enviar e-mail: {str(e)}"
        }
