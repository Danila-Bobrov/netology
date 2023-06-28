import vk_api
from config import user_token, group_token
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
from random import randrange
from data_store import *


def old(years, till=True):
    """Age selection"""
    if till is True:
        name_years = [1, 21, 31, 41, 51, 61, 71, 81, 91, 101]
        if years in name_years:
            return f'{years} года'
        else:
            return f'{years} лет'
    else:
        name_years = [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54, 62, 63, 64]
        if years == 1 or years == 21 or years == 31 or years == 41 or years == 51 or years == 61:
            return f'{years} год'
        elif years in name_years:
            return f'{years} года'
        else:
            return f'{years} лет'


def get_partner_id():
    global unique_person_id, found_persons
    seen_person = []
    for i in check():  # Выбираем из БД просмотренные анкеты.
        seen_person.append(int(i[0]))
    if not seen_person:
        try:  # Если нажать 'Смотреть' без поиска, то будет ошибка, так как list_found_persons изначально пустой.
            unique_person_id = list_found_persons[0]
            return unique_person_id
        except NameError:
            found_persons = 0
            return found_persons
    else:
        try:  # Если нажать 'Смотреть' без поиска, то будет ошибка, так как list_found_persons изначально пустой.
            for ifp in list_found_persons:
                if ifp in seen_person:
                    pass
                else:
                    unique_person_id = ifp
                    return unique_person_id
        except NameError:
            found_persons = 0
            return found_persons


def get_years_of_partner(bdate: str) -> object:
    """User age"""
    bdate_splited = bdate.split(".")
    month = ""
    try:
        reverse_bdate = datetime.date(int(bdate_splited[2]), int(bdate_splited[1]), int(bdate_splited[0]))
        today = datetime.date.today()
        years = (today.year - reverse_bdate.year)
        if reverse_bdate.month >= today.month and reverse_bdate.day > today.day or \
                reverse_bdate.month > today.month:
            years -= 1
        return old(years, False)
    except IndexError:
        if bdate_splited[1] == "1":
            month = "января"
        elif bdate_splited[1] == "2":
            month = "февраля"
        elif bdate_splited[1] == "3":
            month = "марта"
        elif bdate_splited[1] == "4":
            month = "апреля"
        elif bdate_splited[1] == "5":
            month = "мая"
        elif bdate_splited[1] == "6":
            month = "июня"
        elif bdate_splited[1] == "7":
            month = "июля"
        elif bdate_splited[1] == "8":
            month = "августа"
        elif bdate_splited[1] == "9":
            month = "сентября"
        elif bdate_splited[1] == "10":
            month = "октября"
        elif bdate_splited[1] == "11":
            month = "ноября"
        elif bdate_splited[1] == "12":
            month = "декабря"
        return f'День рождения {int(bdate_splited[0])} {month}.'


class Bot:
    def __init__(self):
        print('Bot was created')
        self.vk_user = vk_api.VkApi(
            token=user_token)  # Токен пользователя.
        self.vk_user_got_api = self.vk_user.get_api()  # vk_user подключаем к api.
        self.vk_group = vk_api.VkApi(token=group_token)  # Токен сообщества.
        self.vk_group_got_api = self.vk_group.get_api()  # vk_group подключаем к api.
        self.longpoll = VkLongPoll(
            self.vk_group)  # vk_group_got_api подключаем к Long Poll API для работы с сообществом

    def send_msg(self, user_id, message):
        """Sending messages"""
        self.vk_group_got_api.messages.send(
            user_id=user_id,
            message=message,
            random_id=randrange(10 ** 7)
        )

    def name(self, user_id):
        """Getting the name of the user"""
        user_info = self.vk_group_got_api.users.get(user_id=user_id)
        try:
            name = user_info[0]['first_name']
            return name
        except KeyError:
            self.send_msg(user_id, "Ошибка")

    def looking_age(self, user_id, age):
        global age_from, age_to
        a = age.split("-")
        try:
            age_from = int(a[0])
            age_to = int(a[1])
            if age_from == age_to:
                self.send_msg(user_id, f' Ищем возраст {old(age_to, False)}')
                return
            self.send_msg(user_id, f' Ищем возраст в пределах от {age_from} и до {old(age_to, True)}')
            return
        except IndexError:
            age_to = int(age)
            self.send_msg(user_id, f' Ищем возраст {old(age_to, False)}')
            return
        except NameError:
            self.send_msg(user_id, f' NameError! Введен не правильный числовой формат!')
            return
        except ValueError:
            self.send_msg(user_id, f' ValueError! Введен не правильный числовой формат!')
            return

    def users_age(self, user_id):
        """User age request"""
        global age_from, age_to
        try:
            info = self.vk_user_got_api.users.get(
                user_ids=user_id,
                fields="bdate",
            )[0]['bdate']
            num_age = get_years_of_partner(info).split()[0]
            age_from = num_age
            age_to = num_age
            if num_age == "День":
                print(f'Ваш {get_years_of_partner(info)}')
                self.send_msg(user_id,
                              f'   Бот ищет людей вашего возраста, но в ваших настройках профиля установлен пункт '
                              f'"Показывать только месяц и день рождения"! \n'
                              f'   Поэтому, введите возраст поиска от 21 года и до 35 лет в формате : 21-35 или 21'
                              )
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return self.looking_age(user_id, age)
            return print(f' Ищем вашего возраста {old(age_to)}')
        except KeyError:
            print(f'День рождения скрыт настройками приватности!')
            self.send_msg(user_id,
                          f'   Бот ищет людей вашего возраста, но в ваших настройках профиля установлен пункт '
                          f'"Показывать только месяц и день рождения"! \n'
                          f'   Поэтому, введите возраст поиска от 21 года и до 35 лет в формате : 21-35 или 21'
                          )
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    return self.looking_age(user_id, age)

    def get_city(self, user_id):
        """City of user"""
        global city_id, city_title
        self.send_msg(user_id,
                      f' Введите "Да" - поиск будет произведен в городе указанный в профиле.'
                      f' Или введите название города, например: Челябинск'
                      )
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                answer = event.text.lower()
                if answer == "да" or answer == "y":
                    info = self.vk_user_got_api.users.get(
                        user_id=user_id,
                        fields="city"
                    )
                    city_id = info[0]['city']["id"]
                    city_title = info[0]['city']["title"]
                    return f' в городе {city_title}.'
                else:
                    cities = self.vk_user_got_api.database.getCities(
                        country_id=1,
                        q=answer.capitalize(),
                        need_all=1,
                        count=20
                    )['items']
                    for i in cities:
                        if i["title"] == answer.capitalize():
                            city_id = i["id"]
                            city_title = answer.capitalize()
                            return f' в городе {city_title}'

    def check_gender(self, user_id):
        """Check gender"""
        info = self.vk_user_got_api.users.get(
            user_id=user_id,
            fields="sex"
        )
        if info[0]['sex'] == 1:  # 1 — женщина, 2 — мужчина,
            print(f'Ваш пол женский, ищем мужчину.')
            return 2
        elif info[0]['sex'] == 2:
            print(f'Ваш пол мужской, ищем женщину.')
            return 1
        else:
            print("ERROR!!!")

    def users_search(self, user_id):
        """Partner search"""
        global list_found_persons
        list_found_persons = []
        res = self.vk_user_got_api.users.search(
            sort=0,  # По популярности.
            city=city_id,
            hometown=city_title,
            sex=self.check_gender(user_id),  # 1— женщина, 2 — мужчина, 0 — любой.
            status=1,  # 1 — не женат или не замужем, 6 — в активном поиске.
            age_from=age_from,
            age_to=age_to,
            has_photo=1,  # 1 — искать только пользователей с фотографией, 0 — искать по всем пользователям
            count=20,
            fields="can_write_private_message, "  # Может ли текущий пользователь отправить личное 
            # сообщение. 1 — может; 0 — не может.
                   "city, "  # Информация о городе.
                   "domain, "  # Короткий адрес страницы.
                   "home_town, "  # Родной город.
        )
        number = 0
        for person in res["items"]:
            if not person["is_closed"]:
                if "city" in person and person["city"]["id"] == city_id and person["city"]["title"] == city_title:
                    number += 1
                    id_vk = person["id"]
                    list_found_persons.append(id_vk)
        print(f'Bot found {number} opened profiles for viewing from {res["count"]}')
        return

    def partner_photos(self, user_id):
        """Getting a photo"""
        global attachments
        res = self.vk_user_got_api.photos.get(
            owner_id=user_id,
            album_id="profile",  # wall — фотографии со стены, profile — фотографии профиля.
            extended=1,  # 1 — будут возвращены дополнительные поля likes, comments, tags, can_comment, reposts.
            count=20
        )
        dict_photos = dict()
        for i in res['items']:
            photo_id = str(i["id"])
            i_likes = i["likes"]
            if i_likes["count"]:
                likes = i_likes["count"]
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        attachments = []
        photo_ids = []
        for i in list_of_ids:
            photo_ids.append(i[1])
        try:
            attachments.append('photo{}_{}'.format(user_id, photo_ids[0]))
            attachments.append('photo{}_{}'.format(user_id, photo_ids[1]))
            attachments.append('photo{}_{}'.format(user_id, photo_ids[2]))
            return attachments
        except IndexError:
            try:
                attachments.append('photo{}_{}'.format(user_id, photo_ids[0]))
                return attachments
            except IndexError:
                return print(f'Нет фото')

    def info_partner(self, show_person_id):
        """information about the partner"""
        res = self.vk_user_got_api.users.get(
            user_ids=show_person_id,
            fields="about, "  # «О себе» из профиля.
                   "activities, "  # «Деятельность» из профиля.
                   "bdate, "  # Дата рождения(D.M.YYYY). Если дата рождения скрыта целиком, поле отсутствует в ответе.
                   "status, " # Статус
                   "can_write_private_message, "  # Может ли пользователь отправить личное 
                                                  # сообщение. 1 — может; 0 — не может.
                   "city, "  # Информация о городе партнера.
                   "common_count, "  # Количество общих друзей.
                   "contacts, "  # Информация о телефонных номерах пользователя при обнаружении.
                   "domain, "  # Адрес страницы.
                   "home_town, "  # Родной город.
                   "interests, "  # «Интересы» из профиля.
                   "movies, "  # «Любимые фильмы» из профиля.
                   "music, "  # «Любимая музыка» из профиля.
                   "occupation"  # Информация роде занятия.
        )
        first_name = res[0]["first_name"]
        last_name = res[0]["last_name"]
        age = get_years_of_partner(res[0]["bdate"])
        vk_link = 'vk.com/' + res[0]["domain"]
        city = ''
        try:
            if res[0]["city"]["title"] is not None:
                city = f'Город {res[0]["city"]["title"]}'
            else:
                city = f'Город {res[0]["home_town"]}'
        except KeyError:
            pass
        print(f'{first_name} {last_name}, {age}, {city}. {vk_link}')
        return f'{first_name} {last_name}, {age}, {city}. {vk_link}'

    def send_photo(self, user_id, message, attachments):
        """Sending photos"""
        try:
            self.vk_group_got_api.messages.send(
                user_id=user_id,
                message=message,
                random_id=randrange(10 ** 7),
                attachment=",".join(attachments)
            )
        except TypeError:
            pass

    def partner_check(self, user_id):
        """Show partner from database"""
        print(get_partner_id())
        if get_partner_id() == None:
            self.send_msg(user_id,
                          f'Все анекты ранее были просмотрены. Будет выполнен новый поиск. '
                          f'Измените критерии поиска (возраст, город). '
                          f'Введите возраст поиска в формате: 21-35 или 21 ')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    self.looking_age(user_id, age)
                    self.get_city(user_id)
                    self.users_search(user_id)
                    self.partner_check(user_id)
                    return
        else:
            self.send_msg(user_id, self.info_partner(get_partner_id()))
            self.send_photo(user_id, 'Фото с максимальными лайками',
                            self.partner_photos(get_partner_id()))
            insert_data_seen_partner(get_partner_id())


bot = Bot()
