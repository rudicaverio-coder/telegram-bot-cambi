# bot_cambi_webhook.py - VERSIONE COMPATIBILE 20.6
#GitHub per Gist:  g h p _ q n F F B t U P Y q 0 8 a c r 3 S j j W H w n 5 J i g P C A 2 5 1 i F c
#Github Gist backup:98e323b6ad67035edf13a6d57f97ffe1
# bot_cambi_webhook.py - VERSIONE 13.15 COMPATIBLE
import logging
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# === CONFIGURAZIONE ===
BOT_TOKEN_CAMBI = os.environ.get('BOT_TOKEN_CAMBI')
DATABASE_CAMBI = 'cambi_vvf.db'
MY_USER_ID = 1816045269

# Configurazione logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === DATABASE ===
def init_db_cambi():
    conn = sqlite3.connect(DATABASE_CAMBI)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS vvf (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            qualifica TEXT,
            cognome TEXT,
            nome TEXT,
            autista TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db_cambi()

# === TASTIERA ===
def crea_tastiera_cambi():
    tastiera = [
        [KeyboardButton("👥 VVF"), KeyboardButton("📅 Chi Tocca")],
        [KeyboardButton("🔄 Cambi"), KeyboardButton("🆘 Help")]
    ]
    return ReplyKeyboardMarkup(tastiera, resize_keyboard=True)

# === HANDLER ===
def start_cambi(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != MY_USER_ID:
        update.message.reply_text("❌ Accesso riservato.")
        return
    
    welcome_text = """
🤖 **BOT GESTIONE CAMBI VVF**

Usa i pulsanti per:
• 👥 Gestire i VVF
• 📅 Vedere chi tocca
• 🔄 Gestire i cambi
"""
    update.message.reply_text(welcome_text, reply_markup=crea_tastiera_cambi())

def handle_message_cambi(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id != MY_USER_ID:
        update.message.reply_text("❌ Accesso riservato.")
        return

    if text == "📅 Chi Tocca":
        update.message.reply_text("📅 **CHI TOCCA OGGI**\n\n• 🌙 Sera: S4\n• 🌃 Notte: Bn\n• 🎯 Weekend: C")
    elif text == "👥 VVF":
        mostra_vvf(update)
    elif text == "🆘 Help":
        update.message.reply_text("🆘 **HELP**\n\nUsa i pulsanti per navigare tra le funzioni")
    else:
        update.message.reply_text("ℹ️ Usa i pulsanti qui sotto", reply_markup=crea_tastiera_cambi())

def mostra_vvf(update: Update):
    conn = sqlite3.connect(DATABASE_CAMBI)
    c = conn.cursor()
    c.execute('SELECT cognome, nome, qualifica FROM vvf')
    vvf_lista = c.fetchall()
    conn.close()
    
    if vvf_lista:
        messaggio = "👥 **ELENCO VVF:**\n" + "\n".join([f"• {cognome} {nome} ({qualifica})" for cognome, nome, qualifica in vvf_lista])
    else:
        messaggio = "📝 Nessun VVF nel database. Usa /start per iniziare."
    
    update.message.reply_text(messaggio)

# === MAIN ===
def main_cambi():
    print("🚀 Avvio Bot Gestione Cambi VVF...")
    
    # Crea updater (vecchio stile per v13.15)
    updater = Updater(BOT_TOKEN_CAMBI, use_context=True)
    
    # Aggiungi handler
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_cambi))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message_cambi))
    
    print("🤖 Bot Cambi VVF Avviato!")
    print("📍 Modalità: Polling")
    
    # Avvia polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main_cambi()
