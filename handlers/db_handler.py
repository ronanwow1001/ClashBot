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
    try:
        tmp = db['warnings']
    except:
        print('Startup: implementing warnings')
        db['warnings'] = {}
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

def get_warning_count(userid: int) -> int:
    try:
        tmp = db["warnings"][str(userid)]["count"]
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



verify_sections()