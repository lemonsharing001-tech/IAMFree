import os
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# ----- Render ရဲ့ Environment Variable ကနေ Token ကို ရယူခြင်း -----
TELEGRAM_BOT_TOKEN = os.getenv("8359536332:AAH_214C4jMpBSvkbnyNQKLnL0keL3RXRVU")

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-sh-usage")
    # Server environment မှာ run မှာဖြစ်လို့ Chrome ရဲ့ path ကို တိုက်ရိုက်ညွှန်စရာမလိုပါ
    driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    return driver

def scrape_namso_gen(bin_number):
    url = "https://namso-gen.com/?tab=advance&network=random"
    driver = None
    try:
        driver = setup_driver()
        print(f"Scraping စတင်နေပါပြီ... BIN: {bin_number}")
        driver.get(url)
        time.sleep(3)
        bin_input = driver.find_element(By.ID, "bin")
        bin_input.clear()
        bin_input.send_keys(bin_number)
        generate_button = driver.find_element(By.ID, "btn")
        generate_button.click()
        time.sleep(5)
        result_textarea = driver.find_element(By.ID, "result")
        generated_data = result_textarea.get_attribute("value")
        print("Scraping အောင်မြင်ပါသည်။")
        results_list = generated_data.strip().split('\n')
        if len(results_list) > 15:
            return '\n'.join(results_list[:15])
        else:
            return generated_data
    except Exception as e:
        import traceback
        print("---!!! DETAILED WEBDRIVER ERROR !!!---")
        traceback.print_exc()
        print("---!!! END OF ERROR !!!---")
        error_details = str(e).split('\n')[0]
        return f"⚠️ Bot လုပ်ဆောင်ရာတွင် အမှားဖြစ်ပွားပါသည်။\n\nError: `{error_details}`"
    finally:
        if driver:
            driver.quit()

def start(update, context):
    user = update.effective_user
    update.message.reply_html(f'👋 မင်္ဂလာပါ <b>{user.full_name}</b>!')

def handle_message(update, context):
    user_input = update.message.text
    if user_input.isdigit() and 6 <= len(user_input) <= 16:
        processing_message = update.message.reply_text(f"'{user_input}' အတွက် Generate လုပ်နေပါသည်။ ခဏစောင့်ပါ...")
        result = scrape_namso_gen(user_input)
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=processing_message.message_id)
        update.message.reply_text(f"<b>Generated Results for BIN:</b> <code>{user_input}</code>\n\n<pre>{result}</pre>", parse_mode='HTML')
    else:
        update.message.reply_text("❌ မှားယွင်းနေသော BIN နံပါတ် ဖြစ်ပါသည်။")

def main():
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN ကို Render Environment Variables မှာ ထည့်သွင်းပေးပါ!")
        return
        
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
