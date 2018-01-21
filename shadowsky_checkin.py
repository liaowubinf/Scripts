# -*- coding=UTF-8 -*-
"""Check in on shadowsky.   """
from __future__ import print_function, unicode_literals

import logging
from contextlib import contextmanager
from cookielib import MozillaCookieJar
from getpass import getpass
from os import makedirs
from os.path import dirname, exists, expanduser

from requests import Session

SITE_URL = 'https://www.shadowsky.xyz'
LOGIN_PAGE = '/auth/login'
CHECKIN_PAGE = '/user/checkin'
USER_PAGE = '/user'
COOKIE_PATH = expanduser('~/.shadowsky/cookies')
LOG_PATH = expanduser('~/.shadowsky/.log')
CACHE = {}


@contextmanager
def session():
    """Get global requets session. """

    sess = CACHE.get('session')
    if not isinstance(session, Session):
        sess = Session()
        jar = get_cookie_jar(COOKIE_PATH)
        sess.cookies = jar
        CACHE['session'] = sess
    try:
        yield sess
    finally:
        sess.cookies.save()


def get_cookie_jar(path):
    """Get disk cookie from @path.  """

    jar = CACHE.get('cookies')
    if not isinstance(jar, MozillaCookieJar):
        jar = MozillaCookieJar(path)
        if exists(path):
            jar.load()
        else:
            try:
                makedirs(dirname(path))
            except OSError:
                pass
            jar.save()
        CACHE['cookies'] = jar
    return jar


def is_logged_in():
    """Check if logged in.  """

    url = SITE_URL + USER_PAGE
    with session() as s:
        resp = s.get(url)
    return resp.url == url


def login():
    """CGI login.  """

    url = SITE_URL + LOGIN_PAGE
    payload = {
        'email': raw_input('Email: '),
        'passwd': getpass(str('Password: ')),
        'remember_me': True
    }
    with session() as s:
        resp = s.post(url, data=payload)
    logging.info(resp.json().get('msg'))
    return resp


def checkin():
    """Do check in.  """

    with session() as s:
        resp = s.post(SITE_URL + CHECKIN_PAGE)
    logging.info(resp.json().get('msg'))
    return resp


def main():
    """Script entry.  """

    # setup logging
    handler = logging.FileHandler(LOG_PATH, encoding='UTF-8')
    formatter = logging.Formatter(
        '%(levelname)-6s[%(asctime)s]: %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    while not is_logged_in():
        login()
    checkin()


if __name__ == '__main__':
    main()