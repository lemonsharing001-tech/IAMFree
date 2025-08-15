# Python 3.9 base image ကိုသုံးမယ်
FROM python:3.9-slim

# Google Chrome ကို install လုပ်မယ်
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable

# Chromedriver ကို install လုပ်မယ် (webdriver-manager က ဒါကိုသုံးပါလိမ့်မယ်)
RUN apt-get install -y chromium-driver

# App အတွက် အလုပ်လုပ်မယ့်နေရာတစ်ခု သတ်မှတ်မယ်
WORKDIR /app

# လိုအပ်တဲ့ library စာရင်းကို copy ကူးမယ်
COPY requirements.txt .

# Library တွေကို install လုပ်မယ်
RUN pip install --no-cache-dir -r requirements.txt

# Bot code ကို copy ကူးမယ်
COPY bot.py .

# Container စတင်တဲ့အခါ bot.py ကို run ခိုင်းမယ်
CMD ["python", "bot.py"]
