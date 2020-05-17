import db
import imap
import logging

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, filename='/var/log/dspam-trainer.log', level=logging.INFO)

logging.info('Starting run')
logging.info('Getting users')
dbUsers = db.get_users_from_database()
logging.info('Going to process users')
for u in dbUsers:
    imap.process_user(u[0])

logging.info('Done')
logging.info('==//==')
