# DEBUG LEVEL
DEBUG_LEVEL = 'Info'

# IMAP
IMAP_HOST = 'host.example.com'
IMAP_PORT = 993
IMAP_MASTER_USER = 'dspam_master@not-exist.com'
IMAP_MASTER_PASSWORD = 
IMAP_SPAM_FOLDER = 'Junk'
IMAP_HAM_FOLDER = '"Not Junk"'
IMAP_INBOX_FOLDER = 'Inbox'

# DATABASE
DB_HOST = 'host.example.com'
DB_PORT = 3306
DB_USER = 
DB_PASS = 
DB_DATABASE = 'vmail'

# DSPAM
DSPAM_NO_SIG = 'NOSIG'
DSPAM_CMD = '/opt/dspam/bin/dspam'
DSPAM_SPAM_ACTION = 'spam'
DSPAM_HAM_ACTION = 'innocent'
