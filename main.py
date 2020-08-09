import requests, os, smtplib, ssl, webbrowser


def notify(title, subtitle, text):
    os.system(f'osascript -e \'display notification "{text}" with title "{title}" subtitle "{subtitle}" sound name "Ping"\'')


def send_email(subject, recipient, message):
    port = 465  # For SSL
    sender_email = "michael.automations@gmail.com"
    password = emailPassword
    context = ssl.create_default_context()
    message = f"Subject: {subject}\n{message}"
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, message)


# Start the session
session = requests.Session()

# Get passwords
with open("passwords.txt", "r") as f:
    HackMITPassword = f.readline().strip()
    emailPassword = f.readline().strip()

# Create the payload
payload = {"email":"michael.xu1816@gmail.com",
           "password":HackMITPassword
           }

# Post the payload to the site to log in
s = session.post("https://my.hackmit.org/auth/login", data=payload)
admitted = bool(s.json()["user"]["status"]["admitted"])
declined = bool(s.json()["user"]["status"]["declined"])
waitlisted = bool(s.json()["user"]["status"]["waitlisted"])
name = s.json()["user"]["status"]["name"]

# Notify
if admitted:
    notify("HackMIT Status", name, "Admitted :)")
    send_email("Admitted :) - HackMIT Status", "michael.xu1816@gmail.com", "LETS GO!")
    webbrowser.open_new_tab("https://my.hackmit.org")
elif declined:
    notify("HackMIT Status", name, "Declined :(")
    send_email("Declined :( - HackMIT Status", "michael.xu1816@gmail.com", "Unfortunate")
    webbrowser.open_new_tab("https://my.hackmit.org")
elif waitlisted:
    notify("HackMIT Status", name, "Waitlisted :|")
    send_email("Waitlisted :| - HackMIT Status", "michael.xu1816@gmail.com", "Wait...")
elif s.json()["user"]["status"] != {"completedProfile": True, "admitted": False, "confirmed": False, "declined": False, "checkedIn": False, "reimbursementGiven": False, "waitlisted": False, "name": "submitted"}:
    notify("HackMIT Status", "Update!", s.json()["user"]["status"])
    send_email("Update! - HackMIT Status", "michael.xu1816@gmail.com", s.json()["user"]["status"])
    webbrowser.open_new_tab("https://my.hackmit.org")

