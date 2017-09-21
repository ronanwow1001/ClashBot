import config
from configobj import ConfigObj
import traceback

# This is a singleton-type module and is therefor not a class.
# define variables before methods and move methods around when needed.


db = ConfigObj(infile=config.file_db_name)


# Verify sections to prevent first-start errors.
# Runs every time this is imported but takes little resources.
def verify_sections():
    try:
        tmp = db['link_infractions']
    except:
        print('Startup: implementing link_infractions')
        db['link_infractions'] = {}
    try:
        tmp = db['suggestion_count']
    except:
        print('Startup: implementing suggestion_count')
        db['suggestion_count'] = {}


def add_link_infraction(userid):
    try:
        infractions = int(db['link_infractions'][str(userid)])
    except:
        print(traceback.format_exc())
        infractions = 0
    db['link_infractions'][str(userid)] = str(infractions + 1)
    db.write()


def get_link_infractions(userid):
    try:
        return int(db['link_infractions'][str(userid)])
    except:
        db['link_infractions'][str(userid)] = '0'
        db.write()
        return 0


def add_suggestion_count(userid):
    try:
        infractions = int(db['suggestion_count'][str(userid)])
    except:
        print(traceback.format_exc())
        infractions = 0
    db['suggestion_count'][str(userid)] = str(infractions + 1)
    db.write()


verify_sections()