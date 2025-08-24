import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from email_validator import validate_email, EmailNotValidError
import dns.resolver

load_dotenv()

receiver_mail = os.getenv("RECEIVER_EMAIL")

def send_email(subject:str, body_text:str=None, body_html:str=None, to_email:str=receiver_mail)->bool:
  smpt_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
  port = os.getenv("SMTP_PORT", 587)
  sender_email = os.getenv("SENDER_EMAIL")
  app_password = os.getenv("APP_PASSWORD")

  if not sender_email or not app_password:
    print(f"Error: Missing required credentials.")
    return False

  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = to_email
  message["Subject"] = subject

  if body_html:
    message.attach(MIMEText(body_html, 'html'))
  else:
    message.attach(MIMEText(body_text, 'plain'))
  
  try:
    server = smtplib.SMTP(smpt_server, port)
    server.starttls()
    server.login(sender_email, app_password)
    err = server.send_message(message)
    if err: print(err)
    server.quit()
    print("Email sent successfully")
    return True
  except Exception as e:
    print(f"Failed to deliver email: {e}")
    return False
  

def is_valid_contact_email(email:str)->bool:
  try:
    valid = validate_email(email)
    email = valid.email

    domain = email.split("@")[1]
    dns.resolver.resolve(domain, "MX")
    return True
  except (Exception, EmailNotValidError):
    print(f"Invalid email. Please check your mail {email}")
    return False
  


html_template = '''<table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-family: Arial, sans-serif; background-color: #f6f9fc; padding: 20px;">
  <tr>
    <td align="center">
      <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 8px; padding: 20px;">
        <tr>
          <td align="center" style="padding-bottom: 10px; border-bottom: 1px solid #eee;">
            <img src="{logo}" alt="{company_name} Logo" style="width: 80px; height: auto; margin-bottom: 10px;">
            <h2 style="margin: 10px 0 5px; color: #333;">{role}</h2>
            <p style="margin: 0; color: #666;">at {company_name}</p>
          </td>
        </tr>
        <tr>
          <td style="padding-top: 20px; font-size: 15px; color: #444;">
            <p><strong>Location:</strong> {location}</p>
            <p><strong>Stipend:</strong> {stipend}</p>
            <p><strong>Duration:</strong> {duration}</p>
            <p><strong>Posted:</strong> {post_time}</p>
            <p style="text-align: center;">
              <a href="{apply_link}" target="_blank" style="display: inline-block; margin-top: 15px; padding: 10px 18px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold;">
                Apply Now
              </a>
            </p>
          </td>
        </tr>
        <tr>
          <td style="padding-top: 30px; text-align: center; font-size: 12px; color: #999;">
            Your own daily job and internship updates.
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>'''

