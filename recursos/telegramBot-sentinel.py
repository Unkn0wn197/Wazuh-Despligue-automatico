#Libreria a instalar pip install python-telegram-bot
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Habilitamos Logging.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


#Comando /start
def start(update, context):
    update.message.reply_text("Bot iniciado")


#Comando /help
def help(update, context):
    update.message.reply_text("/start para iniciar el bot. \n /id para ver la ID del chat.")


#Comando /id
def id(update, context):
    id = update.message.chat_id
    update.message.reply_text(id)


#Funcion que escucha los mensajes enviados de wazuh y destaca los que se declaren.
def echo(update, context):
    #Cambio de estado en el servidor de apache
    if "Listened ports status (netstat) changed (new port opened or closed)." in update.message.text:
        update.message.reply_text("@Unkn0wn19"+"⚠️⚠️Incidencia en el servidor de apache ⚠️⚠️")


#Funcion que lanza un error cuando ocurra.
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


#Funcion principal de bot cuando se inicia.
def main():
    updater = Updater("5213603120:AAFnd95-BQpSEAGqBnENorw_NfcudErm4uc", use_context=True)#Token del bot.
    dp = updater.dispatcher
    #Declaracion de los comandos del bot.
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("id", id))
    
    dp.add_handler(MessageHandler(Filters.text, echo))#Log de todos los errores.
    dp.add_error_handler(error)#Inicia el bot.
    updater.start_polling()
    updater.idle()

    
if __name__ == '__main__':
    main()

