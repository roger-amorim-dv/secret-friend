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
# Group pairs by email and prepare consolidated emails
# -----------------------------------------
def group_pairs_by_email(pairs):
    # Group givers by email (who gives to whom)
    email_to_givers = {}
    for p in pairs:
        email = p["giver_email"]
        if email not in email_to_givers:
            email_to_givers[email] = []
        email_to_givers[email].append({
            "name": p["giver_name"],
            "secret_friend": p["receiver_name"]
        })
    
    return email_to_givers


# -----------------------------------------
# Full Execution
# -----------------------------------------
def run_secret_friend(filename, sender_email, sender_password):
    participants = load_participants_from_txt(filename)
    pairs = sort_secret_friend(participants)
    
    # Group pairs by email
    email_to_givers = group_pairs_by_email(pairs)
    
    # Send one email per unique email address
    for email, givers in email_to_givers.items():
        # Build list of names for greeting
        names = [g["name"] for g in givers]
        if len(names) == 1:
            greeting = f"Olá {names[0]}!"
            intro = "Você foi escolhido(a) para o jogo do Secret Friend! 🎁"
        else:
            greeting = f"Olá {', '.join(names[:-1])} e {names[-1]}!"
            intro = "Vocês foram escolhidos(as) para o jogo do Secret Friend! 🎁"
        
        # Build secret friend information
        secret_friend_section = []
        for giver in givers:
            secret_friend_section.append(
                f"👉 {giver['name']}, seu(a) amigo(a) secreto é: {giver['secret_friend']}"
            )
        
        # Build email body
        body = f"""
{greeting}

{intro}

Seu amigo secreto (quem você deve presentear):

{chr(10).join(secret_friend_section)}

Mantenha(m) isso em segredo e divirtam-se!
"""

        send_email(
            sender_email,
            sender_password,
            email,
            "Seu Amigo Secreto 🎁",
            body
        )

    print("✔ Todos os emails enviados!")

if __name__ == "__main__":
    # EDIT THESE
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    run_secret_friend("participants.txt", sender_email, sender_password)
