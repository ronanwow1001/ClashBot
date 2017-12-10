discord_token = ''

admins = [
    '',
    ''
]
sentry_dsn = ''
logs_id = ''
toonhq_id = ''
limiting_role = ''#For Example Rule15
artlimiting_role = ''#For Example Art-no-post
rules_id = ''
gameinfo = ''


#LINKS

# allowed domains, sub-domains of these will also work
allowed_domains = [
    'corpclash.com',
    'judge2020.com',
    'ricky.lol'
]

allowed_channel_domains = {
    '347411900864135189': [
        'youtube.com',
        'youtu.be'
    ]
}

# please keep it lowercase!
links_allowed_roles = [
    'staff',
    'streamer',
    'contributor'
]

#SUGGESTIONS

reaction_channels = {
    # channelid: [array of unicode/custom emotes
    '285072438625042432': ['✅', '❌']
}

#Channels users can't use if limiting role is applied
#Please use their channel names, not ID's
limited_channels = [
    'Suggestions'
]

artlimited_channels = [
    'art'
]

#MODERATION

warn_command_allowed_roles = [
    'staff'
]

command_prefix = '!'

file_db_name = 'users.ini'
