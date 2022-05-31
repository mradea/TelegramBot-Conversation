from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# get API token from BotFather on telegram
# define commands/conversation line like:

NAME = range(1)

def start(update, context):
    update.message.reply_text('Hello, I am a TelegramBot! Use /chat to talk with me!')

def chat(update, context):
    update.message.reply_text('Alright! Please tell me your name first:)')
    return NAME
  
def name(update, context):
    new_name = update.message.text
    context.user_data[name] = new_name
    update.message.reply_text(f'{context.user_data[name}, nice to meet you!')
    return ConversationHandler.END # here you define the endpoint of the conversationhandler
    
def main():
    updater = Updater("API-token",
                      use_context=True)
    dp = updater.dispatcher
    # conversation handler for 'real' conversations
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('chat',chat)], # this is the start command of the conversation
        fallbacks=[],
        # here you can add more states for conversation
        states={
            NAME: [MessageHandler(Filters.text, name)]
            })
    dp.add_handler(conv_handler)
    # command handler for /commands
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

# some commands:
# update.message.reply_text('your message'): send a message
# update.message.text: get last send message
# context.user_data[xy]: store parameters outside of a function
# send documents/plots/figures:
# chat_id = update.message.chat
# document = open('XY','rb')
# context.bot.send_document(chat_id, document)
