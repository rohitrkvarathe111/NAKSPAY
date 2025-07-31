import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

def main_send_email(to_email, subject, body,  body_html=None):
    msg = EmailMessage()
    msg['From'] = os.getenv("EMAIL_HOST_USER")
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)
    if body_html:
        msg.add_alternative(body_html, subtype='html')

    smtp_server = os.getenv("EMAIL_HOST")
    port = int(os.getenv("EMAIL_PORT", 587))
    username = os.getenv("EMAIL_HOST_USER")
    password = os.getenv("EMAIL_HOST_PASSWORD")
    use_tls = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"

    try:
        server = smtplib.SMTP(smtp_server, port)
        if use_tls:
            server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email Sending error: {str(e)}")








def get_welcome_email_html(to_email, verifination_opt):
    try:
        html_content = f"""
        <html>
        <body style="font-family: 'Segoe UI', sans-serif; background-color: #f2f4f8; padding: 40px;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(90deg, #4CAF50, #66BB6A); padding: 30px; color: white; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px;">Welcome, {to_email}!</h1>
                </div>
                <div style="padding: 30px; text-align: center;">
                    <p style="font-size: 18px; color: #333;">We're excited to have you join us!</p>
                    <p style="font-size: 16px; color: #555;">To complete your registration, please use the OTP below:</p>

                    <div style="margin: 30px auto; display: inline-block; background-color: #f1f1f1; padding: 15px 25px; border-radius: 8px; font-size: 24px; font-weight: bold; letter-spacing: 2px; color: #4CAF50;">
                        {verifination_opt}
                    </div>

                    <p style="font-size: 15px; color: #888; margin-top: 20px;">This OTP is valid for only <strong>2 minutes</strong>. Please do not share it with anyone.</p>

                </div>
                <div style="background-color: #f9f9f9; padding: 20px; text-align: center; color: #aaa;">
                    <p style="margin: 0;">&copy; 2025 Your Company. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        subject = "Welcome to NAKSPAY!"
        plain_text = f"Welcome, {to_email}! We're excited to have you with us."
        if main_send_email(to_email, subject, plain_text, html_content):
            return True
        else:
            return False

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error in Content: {str(e)}")



def send_password_reset_email_html(to_email: str, new_password: str, first_name: str):
    try:
        html_content = f"""
        <html>
        <body style="font-family: 'Segoe UI', sans-serif; background-color: #e6f2ec; background-size: cover; background-position: center; background-repeat: no-repeat; padding: 30px;">
            <div style="max-width: 800px; margin: auto; background-color: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.08); border: 1px solid #d4efdf;">
                <div style="background: linear-gradient(90deg, #1abc9c, #16a085); padding: 28px; color: white; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px;">🔐 Password Reset Successful</h1>
                    <p style="margin-top: 10px; font-size: 18px;">Your Rupeer account is secure again</p>
                </div>

                <div style="padding: 25px; text-align: center;">
                    <p style="font-size: 18px; color: #2e4053;">Hello <strong>{first_name}</strong>,</p>
                    <p style="font-size: 16px; color: #5d6d7e; margin-top: 8px;">
                        We’ve successfully reset your password. Please use the new password below to log in to your account.
                    </p>

                    <div style="margin: 25px auto; display: inline-block; background-color: #e8f8f5; padding: 15px 24px; border-radius: 10px; font-size: 22px; font-weight: bold; letter-spacing: 1px; color: #117864; border: 2px dashed #1abc9c;">
                        {new_password}
                    </div>

                    <p style="font-size: 15px; color: #839192; margin-top: 20px;">
                        ⚠️ For your safety, please change this password after logging in and keep it confidential.
                    </p>

                    <a href="www.google.com" target="_blank" style="display: inline-block; margin-top: 25px; padding: 12px 24px; background-color: #1abc9c; color: white; text-decoration: none; font-size: 16px; border-radius: 6px;">
                        🔑 Go to Login
                    </a>
                </div>

                <div style="background-color: #f8f9f9; padding: 18px; text-align: center; color: #aab7b8; font-size: 13px;">
                    <p style="margin: 0;">&copy; 2025 Rupeer. All rights reserved.</p>
                    <p style="margin: 5px 0 0;">Secure your money. Empower your future. 💸</p>
                </div>
            </div>
        </body>
        </html>
        """

        subject = f"Hii {first_name}! Your NAKSPAY Password Has Been Changed"
        plain_text = f"Hello {to_email}, your password has been changed. Your new password is: {new_password}"

        if main_send_email(to_email, subject, plain_text, html_content):
            return True
        else:
            return False

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error in Content: {str(e)}")



# to_email = "rohitvarathe99@gmail.com"
# get_welcome_email_html(to_email, 123456)
