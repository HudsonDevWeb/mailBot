import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import time

class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def enviar_email(self, 
                     destinatarios: List[str], 
                     assunto: str, 
                     html_content: str,
                     delay: float = 0.5) -> dict:
        sucessos = []
        falhas = []
        
        print(f"Iniciando envio para {len(destinatarios)} destinatário(s)...\n")
        
        for i, destinatario in enumerate(destinatarios, 1):
            try:
                msg = MIMEMultipart('alternative')
                msg['From'] = self.email
                msg['To'] = destinatario
                msg['Subject'] = assunto
                
                parte_html = MIMEText(html_content, 'html', 'utf-8')
                msg.attach(parte_html)

                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.email, self.password)
                    server.send_message(msg)
                
                sucessos.append(destinatario)
                print(f"[{i}/{len(destinatarios)}] ✓ Enviado para: {destinatario}")
                
                if i < len(destinatarios):
                    time.sleep(delay)
                    
            except Exception as e:
                falhas.append({'email': destinatario, 'erro': str(e)})
                print(f"[{i}/{len(destinatarios)}] ✗ Erro ao enviar para {destinatario}: {e}")
        
        resultado = {
            'total': len(destinatarios),
            'sucessos': len(sucessos),
            'falhas': len(falhas),
            'emails_enviados': sucessos,
            'emails_falhados': falhas
        }
        
        print(f"\n{'='*50}")
        print(f"RESUMO DO ENVIO")
        print(f"{'='*50}")
        print(f"Total: {resultado['total']}")
        print(f"Sucessos: {resultado['sucessos']}")
        print(f"Falhas: {resultado['falhas']}")
        
        return resultado


def ler_html(caminho_arquivo: str) -> str:

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return f.read()



if __name__ == "__main__":
    SMTP_CONFIG = {
        'smtp_server': 'smtp.gmail.com', 
        'smtp_port': 587,
        'email': 'kutagenda10@gmail.com',
        'password': 'pryz yubi qtar eqgh'
    }
    
    destinatarios = [
        'hudsonmoreiraoliveira501@gmail.com'
    ]
    
    assunto = "Código, impacto e entrega — prazer, Hudson Moreira"
    
    html_content = ler_html('template_email.html')
    
    sender = EmailSender(**SMTP_CONFIG)
    resultado = sender.enviar_email(destinatarios, assunto, html_content)