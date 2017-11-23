discord_token = ''

logs_id = ''
toonhq_id = ''
limiting_role = ''#For Example Rule15
rules_id = ''


#LINKS

# allowed domains, sub-domains of these will also work
allowed_domains = [
    'projectalt.is',
    'projectaltis.com',
    'judge2020.com'
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
    'moderation team',
    'management team',
    'technical team',
    'creative team',
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

#MODERATION

warn_command_allowed_roles = [
    'moderation team',
    'management team',
    'technical team',
    'creative team'
]

command_prefix = '!'

file_db_name = 'users.ini'
