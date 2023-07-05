from datetime import datetime
import vk_api
from vk_api.exceptions import ApiError


class VkTools:
    def __init__(self, acces_token):
        self.api = vk_api.VkApi(token=acces_token)

    def get_profile_info(self, user_id):
        info, = self.api.method('users.get',
                                {'user_id': user_id,
                                 'fields': 'city,bdate,sex,relation,home_town'
                                 }
                                )

        user_info = {'name': info['first_name'] + ' ' + info['last_name'],
                     'id': info['id'],
                     'bdate': info['bdate'] if 'bdate' in info else None,
                     'home_town': info['home_town'] if 'home_town' in info else None,
                     'sex': info['sex'],
                     'city': info['city']['id'] if 'city' in info else None
                     }

        return user_info

    def serch_city(self, city):
        return self.api.method('database.getCities', {'country_id': 1, 'need_all': 1, 'q': city})

    def serch_users(self, params, offset):
        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        curent_year = datetime.now().year
        user_year = int(params['bdate'].split('.')[2])
        age = curent_year - user_year
        age_from = age - 2
        age_to = age + 2
        offset = offset

        users = self.api.method('users.search',
                                {'count': 1,
                                 'offset': offset,
                                 'age_from': age_from,
                                 'age_to': age_to,
                                 'sex': sex,
                                 'city': city,
                                 'status': 6,
                                 'is_closed': False
                                 }
                                )

        try:
            users = users['items']
        except ApiError:
            return []

        res = []

        for user in users:
            if not user['is_closed']:
                res.append({'id': user['id'],
                            'name': user['first_name'] + ' ' + user['last_name']
                            }
                           )

        return res

    def get_photos(self, user_id):
        try:
            photos = self.api.method('photos.get',
                                     {'user_id': user_id,
                                      'album_id': 'profile',
                                      'extended': 1
                                      }
                                     )

        except ApiError as e:
            photos = {}
            print(f'error = {e}')

        result = [{'owner_id': item['owner_id'],
                   'id': item['id'],
                   'likes': item['likes']['count'],
                   'comments': item['comments']['count']
                   } for item in photos['items']
                  ]

        result.sort(key=lambda x: x['likes'] + x['comments'], reverse=True)

        return result[:3]

