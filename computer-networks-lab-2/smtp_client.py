# smtp_client.py
import smtplib
from email.mime.text import MIMEText

def main():
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "sholu1234anuj@gmail.com"   # change
    receiver_email = "sholu0104@gmail.com"  # change
    password = "xnwg zmsg cfua arzu"  # app password, not normal

    try:
        msg = MIMEText("This is a test email from Python SMTP client.")
        msg["Subject"] = "Test Email"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
        server.quit()

    except Exception as e:
        print("SMTP Error:", e)

if __name__ == "__main__":
    main()
