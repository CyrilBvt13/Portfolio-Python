from tinydb import TinyDB, Query

db = TinyDB('config.json')
groups_table = db.table("group")

query = Query()