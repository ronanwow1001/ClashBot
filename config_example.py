discord_token = ''

logs_id = ''

# allowed domains, sub-domains of these will also work
allowed_domains = [
    'projectalt.is',
    'projectaltis.com',
    'judge2020.com'
]

reaction_channels = {
    # channelid: [array of unicode/custom emotes
    '360242743118921738': ['✅', '❌'],
    '285072438625042432': ['✅', '❌']
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

warn_command_allowed_roles = [
    'moderation team',
    'management team',
    'technical team',
    'creative team'
]

exclude_react_starting_character = '`'

command_prefix = '!'

file_db_name = 'users.ini'
