import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -----------------------------------------
# Load participants from TXT
# Format:  Name,Email  (one per line)
# -----------------------------------------
def load_participants_from_txt(filename):
    participants = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if "," not in line:
                continue
            name, email = line.strip().split(",", 1)
            participants.append({
                "name": name.strip(),
                "email": email.strip()
            })
    return participants


# -----------------------------------------
# Shuffle Secret Friends (no self pairing)
# -----------------------------------------
def sort_secret_friend(participants):
    shuffled = participants[:]

    while True:
        random.shuffle(shuffled)
        if all(p["email"] != s["email"] for p, s in zip(participants, shuffled)):
            break

    pairs = []
    for giver, receiver in zip(participants, shuffled):
        pairs.append({
            "giver_name": giver["name"],
            "giver_email": giver["email"],
            "receiver_name": receiver["name"],
            "receiver_email": receiver["email"]
        })

    return pairs


# -----------------------------------------
# Send Email via SMTP
# -----------------------------------------
def send_email(sender_email, sender_password, receiver_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


# -----------------------------------------
# Full Execution
# -----------------------------------------
def run_secret_friend(filename, sender_email, sender_password):
    participants = load_participants_from_txt(filename)
    pairs = sort_secret_friend(participants)

    for p in pairs:
        body = f"""
Olá {p['giver_name']}!

Você foi escolhido(a) para o jogo do Secret Friend! 🎁

Seu(a) amigo(a) secreto é:

👉 {p['receiver_name']}

Mantenha isso em segredo e divirta-se!
"""

        send_email(
            sender_email,
            sender_password,
            p["giver_email"],
            "Seu Amigo Secreto 🎁",
            body
        )

    print("✔ Todos os emails enviados!")

if __name__ == "__main__":
    # EDIT THESE
    sender_email = "your_email@gmail.com"
    sender_password = "password"

    run_secret_friend("participants.txt", sender_email, sender_password)
