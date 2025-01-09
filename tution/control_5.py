from time import sleep

class User:
    def __init__(self, username, password, age):


class Video:
    def __init__(self, title, duration, time_now, adult_mode):


class UrTube:
    def __init__(self, users, videos, current_user):
        self.users = []
        self.videos = []

    def register(self, nickname, password, age):

    def log_out(self):

    def add(self, *args):

    def get_videos(self):

    def watch_video(self):


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Why girls needs for programmer boyfriend?', 10, adult_mode=True)

ur.add(v1, v2)
print(ur.get_videos('лучший'))
print(ur.get_videos('PROG'))

ur.watch_video('Why girls needs for programmer boyfriend?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Why girls needs for programmer boyfriend?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Why girls needs for programmer boyfriend?')

ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

ur.watch_video('Лучший язык программирования 2024 года!')