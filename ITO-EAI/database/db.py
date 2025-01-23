from tinydb import TinyDB, Query

# La database
db = TinyDB('config.json')
query = Query()

# Les tables
groups_table = db.table("group")
flows_table = db.table("flow")

