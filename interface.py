from core import *
from data_store import *

for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = event.user_id
        if request == 'поиск':
            bot.users_age(user_id)
            bot.get_city(user_id)
            bot.users_search(user_id)  # выводит в чат найденных людей и добавляет их в базу данных.
            bot.partner_check(user_id)  # выводит в чат информацию про одного человека из базы данных.
        elif request == 'удалить':
            delete_table_seen_partner()  # удаляет существующую базу данных.
            create_table_seen_partner()  # создает новую базу данных.
            bot.send_msg(user_id, f' База данных удалена! Сейчас наберите "Поиск" ')
        elif request == 'смотреть':
            if get_partner_id() != 0:
                bot.partner_check(user_id)
            else:
                bot.send_msg(user_id, f' В начале наберите Поиск ')
        else:
            bot.send_msg(user_id, f'Здравствуйте, {bot.name(user_id)}. Выберете действие: \n '
                                  f' "Поиск" - Поиск людей. \n'
                                  f' "Удалить" - удалить историю поиска \n'
                                  f' "Смотреть" - смотреть анкеты из истории')
