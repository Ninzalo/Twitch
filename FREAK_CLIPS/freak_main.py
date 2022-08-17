import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from Twitch_v2.main import Twitch
from config import google_login, google_password



if __name__ == '__main__':

    """ SETTINGS """

    # write logs  [ 1 - YES | 0 - NO ]
    write_logs = 1

    # set timer
    # timer_value = "10.00"
    timer_value = None

    # sort by views  [ 1 - YES | 0 - NO ]
    need_to_sort = 1

    # show sorted links if sorting is enabled  [ 1 - YES | 0 - NO ]
    show_sorted = 1

    # max amount of clips
    amount = 20

    # min amount of views
    min_views = 5

    # links to get clips
    twitch_links = [
        'https://www.twitch.tv/pch3lk1n',
        'https://www.twitch.tv/des0ut',
        'https://www.twitch.tv/ekatze007',
        'https://www.twitch.tv/mokrivskyi',
        'https://www.twitch.tv/zloyn',
        'https://www.twitch.tv/ahrinyan',
        'https://www.twitch.tv/yuuechka',
        'https://www.twitch.tv/strogo',
        'https://www.twitch.tv/exileshow',
        'https://www.twitch.tv/karavay46',
        'https://www.twitch.tv/gensyxa',
        'https://www.twitch.tv/buster',
        'https://www.twitch.tv/dmitry_lixxx',
        'https://www.twitch.tv/quickhuntik',
        'https://www.twitch.tv/mapke',
        'https://www.twitch.tv/kostbi4',
        'https://www.twitch.tv/by_owl',
        'https://www.twitch.tv/zark',
        'https://www.twitch.tv/biest1x',
        'https://www.twitch.tv/chr1swave',
        'https://www.twitch.tv/guacamolemolly',
        'https://www.twitch.tv/skillz0r1337',
        'https://www.twitch.tv/fiveskill',
        'https://www.twitch.tv/dinablin',
        'https://www.twitch.tv/indian0ch',
        'https://www.twitch.tv/insider',
        'https://www.twitch.tv/finargot',
        'https://www.twitch.tv/cheatbanned',
        'https://www.twitch.tv/evelone192',
        'https://www.twitch.tv/visshenka',
        'https://www.twitch.tv/fruktozka',
        'https://www.twitch.tv/leron_baron',
        'https://www.twitch.tv/aisumaisu',
        'https://www.twitch.tv/pokanoname',
        'https://www.twitch.tv/koreshzy',
        'https://www.twitch.tv/paradeev1ch',
        'https://www.twitch.tv/shadowkekw'
    ]

    # init class
    my_bot = Twitch(google_login=google_login, google_password=google_password)

    # start uploading
    my_bot.main(my_bot=my_bot, write_logs=write_logs, timer_value=timer_value, need_to_sort=need_to_sort,
                show_sorted=show_sorted, twitch_links=twitch_links, amount=amount, min_views=min_views)
