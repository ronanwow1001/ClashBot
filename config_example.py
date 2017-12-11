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


# Rules

rules = [
    '1) Spamming, swearing, and NSFW talk/images are prohibited in every channel except the NSFW 16+ voice channel.',
    '2) Keep advertising to a minimum, with only one or two posts every now and then. Discord invites are strictly prohibited.',
    '3) Stay on topic in channels that serve a specific purpose such as #groups and #support.',
    '4) Do not spread misinformation such as the servers being up when they are not.',
    '5) Be respectful to other servers. We aren’t here to slander other servers.',
    '6) You are limited to speak only English.',
    '7) Do not attempt to start drama.',
    '8) Be civil to other members. Slander, harassment and aggressive behavior is not allowed.',
    '9) Racism and hate speech is prohibited in every channel.',
    '10) Discussion about leaked sources are not allowed.',
    '11) Do not impersonate staff or any member of the Discord.',
    '12) Do not ask for or share personal information within the Discord.',
    '13) The discussion of politics is not allowed in any of the channels.',
    '14) Backseat moderation is not allowed. If someone is breaking the rules, simply report it to a moderator.',
    '15) Trolling, posting bugs, or other generalized discussions inside of the #suggestions channel will result in an immediate blacklist from posting there.',
    '16) Links of any kind that are not to corpclash.com are not allowed. Bending this rule in any way will also assume you are posting a valid link and will cause it to be deleted.'
]


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
