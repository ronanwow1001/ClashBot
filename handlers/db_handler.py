import config
from configobj import ConfigObj
import traceback

# This is a singleton-type module and is therefor not a class.
# define variables before methods and move methods around when needed.


db = ConfigObj(infile=config.file_db_name)

newid = 0


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
    try:
        tmp = db['warnings']
    except:
        print('Startup: implementing warnings')
        db['warnings'] = {}
    try:
        tmp = db['kicks']
    except:
        print('Startup: implementing kicks')
        db['kicks'] = {}
    try:
        tmp = db['bans']
    except:
        print('Startup: implementing bans')
        db['bans'] = {}
    try:
        tmp = db['bot-warnings']
    except:
        print('Startup: implementing bot-warnings')
        db['bot-warnings'] = {}
        db['bot-warnings']["total"] = 10000
    db.write()


def add_link_infraction(userid: int):
    try:
        infractions = int(db['link_infractions'][str(userid)])
    except:
        print(traceback.format_exc())
        infractions = 0
    db['link_infractions'][str(userid)] = str(infractions + 1)
    db.write()


def get_link_infractions(userid: int) -> int:
    try:
        return int(db['link_infractions'][str(userid)])
    except:
        db['link_infractions'][str(userid)] = '0'
        db.write()
        return 0

def get_bot_warns(warnid):
    try:

        return db['bot-warnings'][str(warnid)]
    except:
        return "Error, no warning with this ID"


def add_suggestion_upvote(userid: int):
    try:
        tmp = db["suggestion_count"][str(userid)]
    except:
        db["suggestion_count"][str(userid)] = {}
    try:
        ups = int(db["suggestion_count"][str(userid)]["ups"])
    except:
        ups = 0
    db["suggestion_count"][str(userid)]["ups"] = str(ups + 1)
    db.write()


def add_suggestion_downvote(userid: int):
    try:
        tmp = db["suggestion_count"][str(userid)]
    except:
        db["suggestion_count"][str(userid)] = {}
    try:
        downs = int(db["suggestion_count"][str(userid)]["downs"])
    except:
        downs = 0
    db["suggestion_count"][str(userid)]["downs"] = str(downs + 1)
    db.write()


def remove_suggestion_upvote(userid: int):
    try:
        tmp = db["suggestion_count"][str(userid)]
    except:
        db["suggestion_count"][str(userid)] = {}
    try:
        ups = db["suggestion_count"][str(userid)]["ups"]
    except:
        ups = 0
    db["suggestion_count"][str(userid)]["ups"] = str(ups - 1)
    db.write()


def remove_suggestion_downvote(userid: int):
    try:
        tmp = db["suggestion_count"][str(userid)]
    except:
        db["suggestion_count"][str(userid)] = {}
    try:
        downs = db["suggestion_count"][str(userid)]["downs"]
    except:
        downs = 0
    db["suggestion_count"][str(userid)]["downs"] = str(downs - 1)
    db.write()



def get_suggestion_upvotes(userid: int) -> int:
    try:
        ups = db["suggestion_count"][str(userid)]["ups"]
    except:
        ups = 0
    return int(ups)


def get_suggestion_downvotes(userid: int) -> int:
    try:
        downs = db["suggestion_count"][str(userid)]["downs"]
    except:
        downs = 0
    return int(downs)


def add_suggestion_count(userid: int):
    try:
        infractions = int(db['suggestion_count'][str(userid)])
    except:
        print(traceback.format_exc())
        infractions = 0
    db['suggestion_count'][str(userid)] = str(infractions + 1)
    db.write()


def add_warning(userid: int, warning: str):
    warning = warning.encode('ascii', 'replace').decode()
    # Ensure their sub-section exists
    try:
        tmp = db["warnings"][str(userid)]
    except:
        db["warnings"][str(userid)] = {}
    # Get/create infraction count
    try:
        infractions = int(db["warnings"][str(userid)]["count"])
    except:
        print(traceback.format_exc())
        db["warnings"][str(userid)]["count"] = 0
        infractions = db["warnings"][str(userid)]["count"]
    infractions += 1
    db["warnings"][str(userid)]["count"] = infractions
    # Set warning reason
    # Kind of hacky but it's a database limitation.
    try:
        db["warnings"][str(userid)]["reason" + str(infractions)] = warning
    except:
        print('UNEXPECTED: exception when defining a new exception')
        print(traceback.format_exc())
    db.write()

def add_kick(userid: int, warning: str):
    warning = warning.encode('ascii', 'replace').decode()
    # Ensure their sub-section exists
    try:
        tmp = db["kicks"][str(userid)]
    except:
        db["kicks"][str(userid)] = {}
    # Get/create infraction count
    try:
        infractions = int(db["kicks"][str(userid)]["count"])
    except:
        print(traceback.format_exc())
        db["kicks"][str(userid)]["count"] = 0
        infractions = db["kicks"][str(userid)]["count"]
    infractions += 1
    db["kicks"][str(userid)]["count"] = infractions
    # Set warning reason
    # Kind of hacky but it's a database limitation.
    try:
        db["kicks"][str(userid)]["reason" + str(infractions)] = warning
    except:
        print('UNEXPECTED: exception when defining a new exception')
        print(traceback.format_exc())
    db.write()

def add_ban(userid: int, warning: str):
    warning = warning.encode('ascii', 'replace').decode()
    # Ensure their sub-section exists
    try:
        tmp = db["bans"][str(userid)]
    except:
        db["bans"][str(userid)] = {}
    # Get/create infraction count
    try:
        infractions = int(db["bans"][str(userid)]["count"])
    except:
        print(traceback.format_exc())
        db["bans"][str(userid)]["count"] = 0
        infractions = db["bans"][str(userid)]["count"]
    infractions += 1
    db["bans"][str(userid)]["count"] = infractions
    # Set warning reason
    # Kind of hacky but it's a database limitation.
    try:
        db["bans"][str(userid)]["reason" + str(infractions)] = warning
    except:
        print('UNEXPECTED: exception when defining a new exception')
        print(traceback.format_exc())
    db.write()

def add_bot_warning(bot_warning: str):
    bot_warning = bot_warning.encode('ascii', 'replace').decode()
    try:
        tmp = db["bot-warnings"]
    except:
        db["bot-warnings"] = {}
        db['bot-warnings']["total"] = str(10000)
    lastid = db["bot-warnings"]["total"]
    global newid
    newid = int(lastid) + 7
    log = str(newid)
    db["bot-warnings"]["total"] = str(newid)
    try:
        db["bot-warnings"][log] = bot_warning
    except:
        print('UNEXPECTED: exception when defining a new exception')
        print(traceback.format_exc())
    db.write()

def get_warning_count(userid: int) -> int:
    try:
        tmp = db["warnings"][str(userid)]["count"]
        return int(tmp)
    except:
        return 0

def get_kicks_count(userid: int) -> int:
    try:
        tmp = db["kicks"][str(userid)]["count"]
        return int(tmp)
    except:
        return 0

def get_bans_count(userid: int) -> int:
    try:
        tmp = db["bans"][str(userid)]["count"]
        return int(tmp)
    except:
        return 0

def get_warnings_text(userid: int) -> str:
    try:
        tmp = int(db["warnings"][str(userid)]["count"])
    except:
        # throws exception when it's not there.
        return 'No warnings'
    mystr = 'Reasons:'
    for i in range(tmp):
        i += 1
        mystr += '\nReason ' + str(i) + ': ' + db["warnings"][str(userid)]["reason" + str(i)]
    return mystr

def get_kicks_text(userid: int) -> str:
    try:
        tmp = int(db["kicks"][str(userid)]["count"])
    except:
        # throws exception when it's not there.
        return 'No warnings'
    mystr = 'Reasons:'
    for i in range(tmp):
        i += 1
        mystr += '\nReason ' + str(i) + ': ' + db["kicks"][str(userid)]["reason" + str(i)]
    return mystr


verify_sections()
