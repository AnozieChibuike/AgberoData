
import requests

def otp(name,email,otp):
    try:
        url = "https://api.sendinblue.com/v3/smtp/email"
        payload = {
            "sender": {
                "name": "noreply@agberodata",
                "email": "developer@agberodata.com"
            },
            "to": [
                {
                    "email": email,
                    "name": name
                }
            ],
            "subject": "Registration Otp",
            "htmlContent": f"<html><head></head><body><p>Hello {name},<br>Thank you for registering with us</p><p>Here is your otp, Please do not share it with anyone.<br><br><p><b>{otp}</b></p><br><br>Best regards,<br><br>AgberoData Team.</p></body></html>"
        }

        headers = {
            "accept": "application/json",
            "api-key": "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",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            return True
        else:
            return response.json()
    except:
        return False


def forgot(name,email,otp):
    try:
        url = "https://api.sendinblue.com/v3/smtp/email"
        payload = {
            "sender": {
                "name": "noreply@agberodata",
                "email": "developer@agberodata.com"
            },
            "to": [
                {
                    "email": email,
                    "name": name
                }
            ],
            "subject": "Forgot Password",
            "htmlContent": f"<html><head></head><body><p>Hello {name},<br>Thank you for reaching us</p><p>Here is your otp, Please do not share it with anyone.<br><br><p><b>{otp}</b></p><br><br>Warmest regards,<br><br>AgberoData Team.</p></body></html>"
        }

        headers = {
            "accept": "application/json",
            "api-key": "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",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            return True
        else:
            return response.json()
    except:
        return False
