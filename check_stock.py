import os
import requests
import smtplib
from email.mime.text import MIMEText

URL = "https://canarypop.es/collections/pre-venta-pokemon-tcg/products/booster-box-30th-celebration-m6a-japones"

def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}/sendMessage",
        params={
            "chat_id": os.environ["TELEGRAM_CHAT_ID"],
            "text": message
        },
        timeout=15
    )

def send_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "🚨 STOCK POKÉMON DISPONIBLE"
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_TO"]

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    server.send_message(msg)
    server.quit()

html = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20
).text.lower()

hay_stock = (
    "añadir al carrito" in html
    or "add to cart" in html
    or "comprar ahora" in html
)

if hay_stock and "agotado" not in html:
    mensaje = f"""🚨 HAY STOCK 🚨

Booster Box Pokémon 30th Celebration M6A Japonés

Compra ya:
{URL}

Este aviso se repetirá cada 5 minutos mientras siga habiendo stock.
"""

    send_telegram(mensaje)
    send_email(mensaje)
    print("Stock detectado. Aviso enviado.")
else:
    print("Sin stock todavía.")
