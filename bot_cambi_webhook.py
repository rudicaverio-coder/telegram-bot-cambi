# bot_cambi_webhook.py - VERSIONE COMPATIBILE 20.6
#GitHub per Gist:  g h p _ q n F F B t U P Y q 0 8 a c r 3 S j j W H w n 5 J i g P C A 2 5 1 i F c
#Github Gist backup:98e323b6ad67035edf13a6d57f97ffe1
import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime
import os
import requests

# === CONFIGURAZIONE ===
BOT_TOKEN_CAMBI = os.environ.get('BOT_TOKEN_CAMBI')
DATABASE_CAMBI = 'cambi_vvf.db'

# ID unico utilizzatore
MY_USER_ID = 1816045269

# Configurazione logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === DATABASE SEMPLIFICATO ===
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

# === TASTIERA FISICA ===
def crea_tastiera_cambi():
    tastiera = [
        [KeyboardButton("👥 Gestisci VVF"), KeyboardButton("📅 Chi Tocca")],
        [KeyboardButton("🔄 Aggiungi Cambio"), KeyboardButton("🆘 Help Cambi")]
    ]
    return ReplyKeyboardMarkup(tastiera, resize_keyboard=True)

# === HANDLER PRINCIPALI ===
async def start_cambi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != MY_USER_ID:
        await update.message.reply_text("❌ Accesso riservato.")
        return
    
    welcome_text = "🤖 **BENVENUTO NEL BOT GESTIONE CAMBI VVF!**"
    await update.message.reply_text(welcome_text, reply_markup=crea_tastiera_cambi())

async def handle_message_cambi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id != MY_USER_ID:
        await update.message.reply_text("❌ Accesso riservato.")
        return

    if text == "📅 Chi Tocca":
        await update.message.reply_text("📅 **CHI TOCCA OGGI**\n\n• Sera: S4\n• Notte: Bn\n• Weekend: C")
    elif text == "👥 Gestisci VVF":
        await mostra_vvf(update)
    elif text == "🆘 Help Cambi":
        await update.message.reply_text("🆘 **HELP**\n\nUsa i pulsanti per navigare")
    else:
        await update.message.reply_text("ℹ️ Usa i pulsanti", reply_markup=crea_tastiera_cambi())

async def mostra_vvf(update: Update):
    conn = sqlite3.connect(DATABASE_CAMBI)
    c = conn.cursor()
    c.execute('SELECT cognome, nome, qualifica FROM vvf')
    vvf_lista = c.fetchall()
    conn.close()
    
    if vvf_lista:
        messaggio = "👥 **ELENCO VVF:**\n" + "\n".join([f"• {cognome} {nome} ({qualifica})" for cognome, nome, qualifica in vvf_lista])
    else:
        messaggio = "📝 Nessun VVF nel database"
    
    await update.message.reply_text(messaggio)

# === MAIN SEMPLIFICATO ===
def main_cambi():
    print("🚀 Avvio Bot Gestione Cambi VVF...")
    
    # Crea application
    application = Application.builder().token(BOT_TOKEN_CAMBI).build()
    
    # Aggiungi handler
    application.add_handler(CommandHandler("start", start_cambi))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_cambi))
    
    print("🤖 Bot Cambi VVF Avviato!")
    print("📍 Modalità: Polling")
    
    # Avvia con polling
    application.run_polling()

if __name__ == '__main__':
    main_cambi()
