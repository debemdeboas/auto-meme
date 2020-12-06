from dotenv import load_dotenv
from image import _Image
from instagram_poster import InstagramPoster
from pathlib import Path
from threading import Thread
from typing import List

import arrow
import os
import praw
import requests
import time
import utils



class Scalper(Thread):
    def __init__(self) -> None:
        super(Scalper, self).__init__(daemon=True)
        self._images = []
        self._reddit_d = reddit_login(
            *get_user_credentials('REDDIT_CREDENTIALS'))
        self._timeout = 8 * 60

    def run(self) -> None:
        while True:
            # remove stale memes
            for file in Path('images/').glob('*'):
                if arrow.get(file.stat().st_mtime) > arrow.now().shift(hours=+1):
                    os.remove(file)

            # get next meme
            post = next(self._reddit_d.subreddit('memes').new(limit=1))
            skip = False
            for img in self._images:
                if img.caption == post.title:
                    os.remove(img.path)
                    skip = True
            if skip:
                continue

            # download the maymay
            r = requests.get(post.url, stream=True)
            if r.status_code != 200:
                time.sleep(self._timeout / 2)
                continue
            r.raw.decode_content = True
            tmp_path = utils.save_image(r.raw)
            path = utils.prepare_image(tmp_path)
            self.images.append(_Image(path, post.title))

            time.sleep(self._timeout)

    @property
    def images(self): return self._images


def load_env() -> None:
    load_dotenv()


def get_user_credentials(env_var: str) -> List[str]:
    return os.getenv(env_var).split(',')


def reddit_login(id: str, secret: str) -> praw.Reddit:
    return praw.Reddit(
        client_id=id,
        client_secret=secret,
        user_agent='reddit_poller'
    )


if __name__ == "__main__":
    load_env()
    scalper_daemon = Scalper()
    instagram_daemon = InstagramPoster(
        scalper_daemon.images, *get_user_credentials('INSTA_CREDENTIALS'))

    scalper_daemon.start()
    instagram_daemon.run()
