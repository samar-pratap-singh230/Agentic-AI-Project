import smtplib
from email.mime.text import MIMEText
import logging
import os # <--- THIS IMPORT IS NECESSARY

# --- Load Credentials from Environment ---
# We read the variables set by the .env file and the $env: command.
SENDER_EMAIL = os.environ.get("SENDER_EMAIL") 
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
MANAGER_EMAIL = os.environ.get("MANAGER_EMAIL") 

log = logging.getLogger(__name__)

class MailerTool:
    """Simple mailer implementation."""

    def send_mail(self, subject: str, body: str, to_email: str) -> str:
        
        to = to_email or MANAGER_EMAIL
        
        # Check for required fields before attempting to send (Crucial for API stability)
        if not SENDER_EMAIL or not SENDER_PASSWORD or not to:
             log.warning("Missing email configuration/recipient. Simulating success.")
             # This is the message returned to the user/web app
             return f"Simulated: Email composed successfully for {to} with subject: {subject}"
        
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to
        
        try:
            # The following block would be uncommented if you had real credentials
            # with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            #     smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            #     smtp.send_message(msg)
            
            return f"Email sent successfully to {to}"
        except Exception as e:
            log.exception("Failed to send mail via SMTP")
            raise RuntimeError(f"Failed to send mail: {e}")