import pandas as pd
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import uncertainties as un
from uncertainties import ufloat
from uncertainties import unumpy
import os


#first, you'll need to create a csv file with the columns: Date, Train, Duration, Delay, Cancelled, Reason
# this is the empty csv:
df = pd.read_csv('Trains.csv')
#print (df)

DATE, TRAIN, DURATION, DELAY, CANCELLED, REASON, GETQUERY, STATS1, MORE, STATS2 = range(10) 

def help(update, context):
    update.message.reply_text('''
Please use the following commands:
/entry: Make a new entry
/stats: See some statistics/diagrams and stuff''')

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

def stats(update, context):
    update.message.reply_text('''Okay, let's look at some stats. What do you want to know? You can choose whether I tell you something about /specific trains or /general information.''')

def specific(update, context):
    update.message.reply_text('Very well. Please tell me the name of the train you want to know about, e.g. RE 7!')
    return GETQUERY

def get_query(update, context):
    qry = update.message.text
    cud = context.user_data
    cud[query] = qry.lower()
    update.message.reply_text('Thank you very much, I will look up the information right now...')
    return STATS1

def stats1(update, context):
    query = cud[query]
    data = df.loc[df['Train'].str.contains(f'{query}', case=False)]
    mean_delay = np.mean(data['Delay [min]'])
    max_delay = np.max(data['Delay [min]'])
    ratio = data['Delay [min]']/(data['Duration [h]']*60)
    ratio_mean = np.mean(ratio)
    update.message.reply_text(
f'''Stats about {query}:
Mean delay: {mean_delay}
Max delay: {max_delay}
Ratio (delay/normal duration): {ratio_mean}''')
    return ConversationHandler.END

def general(update, context):
    update.message.reply_text('Very well, I will give you an overview.')
    mean_delay = np.mean(df['Delay [min]'])
    mean_ratio = np.mean(df['Delay [min]']/df['Duration [h]']*60)
    max_delay = np.max(df['Delay [min]'])
    max_train_row = df.loc[df['Train.csv'].str.contains(f'{max_delay}', case=False]
    max_train = max_train_row['Train']
    max_train_date = max_train_row['Date']
    update.message.reply_text(f'''
Mean delay: {mean_delay}
Mean ratio: {mean_ratio}
Max delay: {max_delay}, train: {max_train}, date: {max_train_date}
''')
    update.message.reply_text('Do you want to know more?')
    return MORE

def more(update, context):
    cud = context.user_data
    answer = update.message.text
    cud[answer] = answer.lower()
    if cud[answer] == 'no':
        update.message.reply_text('Have a good day!')
    else:
        return STATS2

def stats2(update, context):
    mean_delayRE = np.mean(df[df['Delay [min]'].str.contains('re', regex=False)])
    std_delayRE = np.std(df[df['Delay [min]'].str.contains('re', regex=False)])
    mean_delayICE = np.mean(df[df['Delay [min]'].str.contains('ice', regex=False)])
    std_delayICE = np.std(df[df['Delay [min]'].str.contains('ice', regex=False)])
    mean_delayIC = np.mean(df[df['Delay [min]'].str.contains('ic', regex=False)])
    std_delayIC = np.std(df[df['Delay [min]'].str.contains('ic', regex=False)])
    mean_delayEC = np.mean(df[df['Delay [min]'].str.contains('ec', regex=False)])
    std_delayEC = np.std(df[df['Delay [min]'].str.contains('ec', regex=False)])
    mean_delayS = np.mean(df[df['Delay [min]'].str.contains('s', regex=False)])
    std_delayS = np.std(df[df['Delay [min]'].str.contains('s', regex=False)])
    type = [RE, ICE, IC, EC, S]
    mean_delays = [mean_delayRE, mean_delayICE, mean_delayIC, mean_delayEC, mean_delayS]
    std_delays = [std_delayRE, std_delayICE, std_delayIC, std_delayEC, std_delayS]
    plt.bar(type, mean_delays, yerr=std_delays)
    plt.ylabel('Delay [min]')
    plt.savefig('XY')
    chat_id = update.message.chat_id
    document = open('XY','rb')
    context.bot.send_document(chat_id, document)
    update.message.reply_text('Here you can see the average delays of different train types.')
    os.remove('XY')
    return ConversationHandler.END

def main():
    # you'll need to get your API token from Telegram BotFather
    updater = Updater("Your_token",
                      use_context=True)
    dp = updater.dispatcher
    #define conversation handler with entry point and message handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('entry',entry)],
        fallbacks=[],
        states={
            DATE: [MessageHandler(Filters.text,date)],
            TRAIN: [MessageHandler(Filters.text,train)],
            DURATION: [MessageHandler(Filters.text,duration)],
            DELAY: [MessageHandler(Filters.text,delay)],
            CANCELLED: [MessageHandler(Filters.text,cancelled)],
            REASON: [MessageHandler(Filters.text, reason)]})
     conv_handler2 = [ConversationHandler(
        entry_points=[CommandHandler('specific', specific)],
        fallbacks=[],
        states={
            GETQUERY: [MessageHandler(Filters.text, get_query)],
            STATS1: [MessageHandler(Filters.text, stats1)]})]
     conv_handler3 = [ConversationHandler(
        entry_points=[CommandHandler('general', general)],
        fallbacks=[],
        states={
            MORE: [MessageHandler(Filters.text, more)],
            STATS2: [MessageHandler(Filters.text, stats2)]}
            )]
    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler2)
    dp.add_handler(conv_handler3)
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('stats', stats))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
