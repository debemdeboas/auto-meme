from pathlib import Path
from typing import List

import instabot
import time



class InstagramPoster():
    default_hashtags = '#meme #funny #lol #lmao #dog #cute #reddit #tiktok #foryou #cat #haha #happy #tbt #instagood #photooftheday #smile #igers #amazing #bot #follow #followme #like4like #instamood'

    def __init__(self, imgs: List, usr, pwd) -> None:
        self.images = imgs
        self._ig = instabot.Bot()
        self.login(usr, pwd)
        self._timeout = 30 * 60 # 30 minutes

    def login(self, usr, pwd) -> bool:
        return self._ig.login(username=usr, password=pwd)

    def post_photo(self, path, caption) -> bool:
        return self._ig.upload_photo(Path(path).resolve(), f'{caption}\n.\n{self.default_hashtags}')

    def run(self) -> None:
        while True:
            if len(self.images) <= 0:
                time.sleep(self._timeout)
                continue
            img = self.images.pop()
            print(img)
            self.post_photo(img.path, img.caption)
            time.sleep(self._timeout)
