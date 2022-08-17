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
        'https://www.twitch.tv/mibrozzz',
        'https://www.twitch.tv/bratishkinoff',
        'https://www.twitch.tv/razdva',
        'https://www.twitch.tv/mazellovvv',
        'https://www.twitch.tv/gwinglade',
        'https://www.twitch.tv/grpzdc',
        'https://www.twitch.tv/sindicsgo',
        'https://www.twitch.tv/lagoda1337',
        'https://www.twitch.tv/nelyaray',
        'https://www.twitch.tv/karandashaa',
        'https://www.twitch.tv/lomaka',
        'https://www.twitch.tv/pinkbutterflyman',
        'https://www.twitch.tv/muhanjan',
        'https://www.twitch.tv/batyaoffc',
        'https://www.twitch.tv/silazhik',
        'https://www.twitch.tv/t2x2',
        'https://www.twitch.tv/jesusavgn',
        'https://www.twitch.tv/drakeoffc',
        'https://www.twitch.tv/superstas2',
        'https://www.twitch.tv/stintik',
        'https://www.twitch.tv/dinik',
        "https://www.twitch.tv/baragozzers",
        "https://www.twitch.tv/jojohf",
        "https://www.twitch.tv/cirilla04",
        'https://www.twitch.tv/gaechkatm',
        'https://www.twitch.tv/stanislaw9'
    ]

    # init class
    my_bot = Twitch(google_login=google_login, google_password=google_password)

    # start uploading
    my_bot.main(my_bot=my_bot, write_logs=write_logs, timer_value=timer_value, need_to_sort=need_to_sort,
                show_sorted=show_sorted, twitch_links=twitch_links, amount=amount, min_views=min_views)
    # print(my_bot.google_login())
