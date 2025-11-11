import smtplib
import ssl
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def carregar_configuracoes():
    """Carrega as configurações do arquivo .env"""
    load_dotenv()
    return {
        'email_remetente': os.getenv('EMAIL_REMETENTE'),
        'senha_app': os.getenv('SENHA_APP'),
        'smtp_servidor': os.getenv('SMTP_SERVIDOR', 'smtp.gmail.com'),
        'smtp_porta': int(os.getenv('SMTP_PORTA', 587))
    }

def carregar_destinatarios(arquivo='destinatarios.csv'):
    """Carrega a lista de destinatários de um arquivo CSV"""
    try:
        df = pd.read_csv(arquivo)
        return df.to_dict('records')
    except FileNotFoundError:
        print(f"Erro: Arquivo {arquivo} não encontrado.")
        return []

def enviar_email(remetente, senha, destinatario, assunto, corpo, smtp_servidor, smtp_porta):
    """Envia um único e-mail"""
    try:
        # Criando a mensagem
        mensagem = MIMEMultipart()
        mensagem['From'] = remetente
        mensagem['To'] = destinatario['email']
        mensagem['Subject'] = assunto
        
        # Adicionando o corpo da mensagem
        mensagem.attach(MIMEText(corpo, 'plain'))
        
        # Criando conexão segura com o servidor SMTP
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_servidor, smtp_porta) as servidor:
            servidor.starttls(context=context)
            servidor.login(remetente, senha)
            servidor.send_message(mensagem)
            
        print(f"E-mail enviado para {destinatario['email']} - {destinatario.get('nome', '')}")
        return True
        
    except Exception as e:
        print(f"Erro ao enviar e-mail para {destinatario.get('email', '')}: {str(e)}")
        return False

def carregar_template(arquivo='email_template.txt'):
    """Carrega o assunto e o conteúdo do e-mail de um arquivo de template"""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        # Separa o assunto (primeira linha) do corpo do e-mail
        linhas = conteudo.split('\n', 1)
        assunto = linhas[0].replace('ASSUNTO:', '').strip()
        corpo = linhas[1].strip() if len(linhas) > 1 else ''
        return assunto, corpo
    except FileNotFoundError:
        return None, None

def main():
    # Carregar configurações
    config = carregar_configuracoes()
    
    # Verificar se as configurações necessárias foram fornecidas
    if not all([config['email_remetente'], config['senha_app']]):
        print("Erro: Configure corretamente as variáveis de ambiente no arquivo .env")
        print("É necessário configurar EMAIL_REMETENTE e SENHA_APP")
        return
    
    # Carregar lista de destinatários
    destinatarios = carregar_destinatarios()
    if not destinatarios:
        print("Nenhum destinatário encontrado. Verifique o arquivo 'destinatarios.csv'")
        return
    
    # Carregar template do e-mail
    assunto, corpo_template = carregar_template()
    if assunto is None or corpo_template is None:
        print("Erro: Não foi possível carregar o template do e-mail. Verifique o arquivo 'email_template.txt'")
        return
    
    # Confirmar envio
    confirmacao = input(f"\nDeseja enviar {len(destinatarios)} e-mail(s) com o assunto '{assunto}'? (s/n): ")
    if confirmacao.lower() != 's':
        print("Envio cancelado.")
        return
    
    # Enviar e-mails
    enviados = 0
    for destinatario in destinatarios:
        if enviar_email(
            config['email_remetente'],
            config['senha_app'],
            destinatario,
            assunto,
            # Substitui {nome} pelo nome do destinatário no corpo do e-mail
            corpo_template.format(nome=destinatario.get('nome', '')),
            config['smtp_servidor'],
            config['smtp_porta']
        ):
            enviados += 1
    
    print(f"\nProcesso concluído! {enviados} de {len(destinatarios)} e-mails foram enviados com sucesso.")

if __name__ == "__main__":
    print("=== Sistema de Envio de E-mails em Massa ===\n")
    main()
