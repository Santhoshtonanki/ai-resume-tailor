import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

message = """🌍 Strategic Global Job Alert

🎯 Target: Remote + Sponsorship + Relocation

🔹 Platform Engineer
🏢 GitLab
📍 Remote Worldwide
🎯 Match: 91%
📄 Use: DevOps Global Resume

🔹 Cloud Operations Engineer
🏢 Canonical
📍 Europe / Remote
🎯 Match: 88%
📄 Use: Cloud Global Resume

🔹 Kubernetes Engineer
🏢 Shopify
📍 Remote
🎯 Match: 86%
📄 Use: DevOps Global Resume

🚀 Daily target: 20 applications
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": message})
