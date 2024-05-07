from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from starlette.background import BackgroundTasks
from app.core.config import settings
from pathlib import Path

class Mail:
  conf = None
  def __init__(
    self,
    mail_username=settings.MAIL_USERNAME,
    mail_password=settings.MAIL_PASSWORD,
    mail_from=settings.MAIL_FROM,
    mail_port=settings.MAIL_PORT,
    mail_sever=settings.MAIL_SERVER,
    mail_server_name=settings.MAIL_FROM_NAME,
    mail_ssl_tls=settings.MAIL_SSL_TLS,
    mail_starttls=settings.MAIL_STARTTLS,
    use_credentials=settings.USE_CREDENTIALS,
    mail_debug=settings.MAIL_DEBUG,
    template_folder=Path(__file__).parent.parent / 'templates/mail',
  ):
    self.conf = ConnectionConfig(
      MAIL_USERNAME=mail_username,
      MAIL_PASSWORD=mail_password,
      MAIL_FROM=mail_from,
      MAIL_PORT=mail_port,
      MAIL_SERVER=mail_sever,
      MAIL_FROM_NAME=mail_server_name,
      MAIL_SSL_TLS=mail_ssl_tls,
      USE_CREDENTIALS=use_credentials,
      MAIL_STARTTLS=mail_starttls,
      MAIL_DEBUG=mail_debug,
      TEMPLATE_FOLDER=template_folder
    )
  
  async def send_email_async(self, subject: str, email_to: str, body: str, template_body: dict):
    message = MessageSchema(
      subject=subject,
      recipients=[email_to],
      body=body,
      template_body=template_body,
      subtype=MessageType.html
    )
    
    print('hello>>>',self)
    fm = FastMail(self.conf)
    await fm.send_message(message, template_name='email.html')

  def send_email_background(self, background_tasks: BackgroundTasks, subject: str, email_to: str, body: str, template_body: dict):
    message = MessageSchema(
      subject=subject,
      recipients=[email_to],
      body=body,
      template_body=template_body,
      subtype=MessageType.html,
    )
    fm = FastMail(self.conf) 
    background_tasks.add_task(
       fm.send_message, message, template_name='email.html')

