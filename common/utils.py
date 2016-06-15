# -*- coding: utf-8 -*-
import os.path
import sys
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import hashlib
import mongoengine
import settings


def connect_db():
    mongoengine.connect(settings.DB_NAME, host=settings.DB_ADDRESS, port=settings.DB_PORT)


def md5(astring):
    return hashlib.md5(astring).hexdigest()


def make_card_id():
    import pymongo
    conn = pymongo.Connection('localhost', 27017)
    db = conn.office
    card_coll = db.card_id

    # card_coll.save({"card_id": 10000})
    new_id = card_coll.find_and_modify(update={"$inc": {"card_id": 1}}, new=True).get("card_id")
    print new_id
    return new_id

if __name__ == "__main__":
    # print md5('2222')
    make_card_id()
