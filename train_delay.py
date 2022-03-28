import pandas as pd
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

#first, you'll need to create a csv file with the columns: Date, Train, Duration, Delay, Cancelled, Reason
# this is the empty csv:
df = pd.read_csv('Trains.csv')
print (df)

ENTRY, DATE, TRAIN, DURATION, DELAY, CANCELLED, REASON = range(7)

def start(update, context):
    update.message.reply_text('Hi! I will track your train delays! Use /entry to make a new entry')
    return ENTRY

def entry(update, context):
    update.message.reply_text('''So, your train is late again. A pity. To document the delay, please let me know today's date!''')
    return DATE

def date(update, context):
    d = update.message.text
    # store user reply as context
    context.user_data[date] = d.lower()
    update.message.reply_text('And your train was called...?')
    return TRAIN

def train(update, context):
    t = update.message.text
    context.user_data[train] = t.lower()
    update.message.reply_text('What was the normal duration [h]?')
    return DURATION

def duration(update, context):
    drt = update.message.text
    context.user_data[duration] = drt.lower()
    update.message.reply_text('Okay, how many minutes was the train late? If the train was cancelled, please enter 0.')
    return DELAY

def delay(update, context):
    dly = update.message.text
    context.user_data[delay] = dly.lower()
    update.message.reply_text('Was your train cancelled? Please answer "yes" or "no".')
    return CANCELLED

def cancelled(update, context):
    cld = update.message.text
    context.user_data[cancelled] = cld.lower()
    update.message.reply_text('Was there a reason why the train was late/cancelled? Please enter "no", if there was no delay.')
    return REASON

def reason(update, context):
    rsn = update.message.text
    context.user_data[reason] = rsn.lower()
    update.message.reply_text('Thank you very much, I will now store your information...')
    # store data as csv file using pandas
    cud = context.user_data
    data = {'Date': [f'{cud[date]}'],
            'Train': [f'{cud[train]}'],
            'Duration': [f'{cud[duration]}'],
            'Delay': [f'{cud[delay]}'],
            'Cancelled': [f'{cud[cancelled]}'],
            'Reason': [f'{cud[reason]}']}
    new_entry = pd.DataFrame(data)
    new_entry.to_csv('Trains.csv', mode='a', index=False, header=False)
    df = pd.read_csv('Trains.csv')
    update.message.reply_text('Done! Thanks for participating! If you want to make a new entry, please /start the conversation.')
    #print(df) to verify the updated csv file
    return ConversationHandler.END

def main():
    # you'll need to get your API token from Telegram BotFather
    updater = Updater("Your_token",
                      use_context=True)
    dp = updater.dispatcher
    #define conversation handler with entry point and message handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        fallbacks=[],
        states={
            ENTRY: [CommandHandler('entry',entry)],
            DATE: [MessageHandler(Filters.text,date)],
            TRAIN: [MessageHandler(Filters.text,train)],
            DURATION: [MessageHandler(Filters.text,duration)],
            DELAY: [MessageHandler(Filters.text,delay)],
            CANCELLED: [MessageHandler(Filters.text,cancelled)],
            REASON: [MessageHandler(Filters.text, reason)]})
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('help',help))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
