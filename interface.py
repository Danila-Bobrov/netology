import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from core import VkTools
from data_store import *
from config import acces_token, community_token


class BotInterface:
    def __init__(self, community_token, acces_token):
        self.interface = vk_api.VkApi(token=community_token)
        self.api = VkTools(acces_token)
        self.users_info_profile = {}
        self.offset = 0

    def message_get(self):
        return self.interface.method('messages.get',
                                     {'count': 1
                                      }
                                     )

    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id()
                               }
                              )

    def event_handler(self):
        longpoll = VkLongPoll(self.interface)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if event.user_id not in self.users_info_profile:
                    params = self.api.get_profile_info(event.user_id)
                    self.users_info_profile[event.user_id] = {'params': params}
                    params_list = self.users_info_profile[event.user_id]['params']

                    for data in params_list:
                        if params_list[data] is None:
                            self.message_send(event.user_id, f'напишите {data}:')

                            for i in longpoll.listen():
                                if i.type == VkEventType.MESSAGE_NEW and i.to_me:
                                    city = i.text
                                    for city_user in self.api.serch_city(city)['items']:
                                        if city_user['title'] == city:
                                            params_list[data] = city_user['id']
                                    print(params_list)
                                    break

                if command == 'привет':
                    self.message_send(event.user_id, f'Здравствуй, '
                                                     f'{self.users_info_profile[event.user_id]["params"]["name"]}\n'
                                                     f'Для поиска введите "Поиск"\n'
                                                     f'Для удаления истории поиска введите "Удалить"'
                                      )
                elif command == 'поиск':
                    dict_params = self.users_info_profile[event.user_id]['params']
                    create_db_users_base()
                    users = self.api.serch_users(dict_params, self.offset)

                    while len(users) == 0:
                        self.offset += 1
                        users = self.api.serch_users(dict_params, self.offset)
                    user = users[0]
                    self.message_send(event.user_id, f'Начинаем поиск')
                    photos_user = self.api.get_photos(user['id'])
                    attachment = []

                    for num, photo in enumerate(photos_user):
                        attachment.append(f'photo{photo["owner_id"]}_{photo["id"]}')
                        if num == 2:
                            break
                    user_id = 'id' + str(user['id'])
                    self.message_send(event.user_id,
                                      f'Встречайте: {user["name"]}',
                                      attachment=','.join(attachment)
                                      )
                    self.message_send(event.user_id, f'Ссылка: vk.com/id{user["id"]}')
                    self.offset += 1

                    try:
                        insert_data_users_base(user_id)
                    except:
                        pass

                elif command == 'удалить':
                    delete_users_base()
                    create_db_users_base()
                    self.message_send(event.user_id, f'История поиска удалена')

                elif command == 'пока':
                    self.message_send(event.user_id, f'Досвидания, '
                                                     f'{self.users_info_profile[event.user_id]["params"]["name"]}.\n'
                                                     f' До новых встречь')

                else:
                    self.message_send(event.user_id, f'{self.users_info_profile[event.user_id]["params"]["name"]}, '
                                                     f'команда не опознана\n'
                                                     f'Для поиска введите "Поиск"\n'
                                                     f'Для удаления истории поиска введите "Удалить"'
                                      )


if __name__ == '__main__':
    bot = BotInterface(community_token, acces_token)
    print('Bot was created!')
    bot.event_handler()
