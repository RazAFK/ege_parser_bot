import telebot, gspread
from settings import token, google_client, test_url, table_url
from url_parser import get_results

bot = telebot.TeleBot(token)

def process_data(surname, date, link, url, gc: gspread.Client=google_client):
    sh = gc.open_by_url(url)
    worksheet = sh.get_worksheet(0)
    try:
        varnum, score, wrong = get_results(link)
    except Exception as e:
        return 'Ошибка! Неверная ссылка' + f'\n{e}'
    row = worksheet.find(surname)
    if row is None: return 'Ошибка! Неверная фамилия'
    col = worksheet.find(date)
    if col is None: return 'Ошибка! Неверная дата'
    row = row.row
    col = col.col
    if all((worksheet.cell(row, col).value is not None,
           worksheet.cell(row, col+1).value is not None,
           worksheet.cell(row, col+2).value is not None)):
        if all((worksheet.cell(row+1, col).value is not None,
           worksheet.cell(row+1, col+1).value is not None,
           worksheet.cell(row+1, col+2).value is not None)):
            return 'Ошибка! Для этой даты все ячейки заняты'
        
        worksheet.update_cell(row+1, col, varnum)
        worksheet.update_cell(row+1, col+1, wrong)
        worksheet.update_cell(row+1, col+2, score)
        return 'Вариант добавлен'
    
    worksheet.update_cell(row, col, varnum)
    worksheet.update_cell(row, col+1, wrong)
    worksheet.update_cell(row, col+2, score)
    return 'Вариант добавлен'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Пришлите сообщение в формате, каждое на новой строке(всё в точности как в документе):\nФамилия\nДата\nСсылка на страницу с результатом(только Решу ЕГЭ)')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        parts = message.text.split(sep='\n')
        if len(parts) == 3:
            surname, date, link = parts
            result = process_data(surname, date.strip(), link, test_url)
            bot.reply_to(message, result)
        else:
            bot.reply_to(message, 'Ошибка! Введите три значения, каждое на новой строке(всё в точности как в документе):\nФамилия\nДата\nСсылка на страницу с результатом(только Решу ЕГЭ)')
            
    except Exception as e:
        bot.reply_to(message, f'Ошибка!\n{e}')

if __name__ == '__main__':
    print('started')
    bot.infinity_polling()
