import constants
import logging
import ssl
import subprocess
from imaplib import IMAP4_SSL


def process_user(emailAddress):
    logging.info('Processing: %s', emailAddress)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()

    M = IMAP4_SSL(host=constants.IMAP_HOST, port=constants.IMAP_PORT, ssl_context=context)
    logging.info('IMAP connection made')
    # construct the user login
    userLogin = emailAddress + '*' + constants.IMAP_MASTER_USER

    M.login(userLogin, constants.IMAP_MASTER_PASSWORD)
    logging.info('User logged in')

    M.select(constants.IMAP_SPAM_FOLDER)
    process_folder(M, constants.DSPAM_SPAM_ACTION, emailAddress)

    M.select(constants.IMAP_HAM_FOLDER)
    process_folder(M, constants.DSPAM_HAM_ACTION, emailAddress)
    M.expunge()
    M.close()
    M.logout()

def process_folder(mailbox, action, user):
    logging.info('Processing folder with action: %s', action)
    typ, data = mailbox.search(None, 'UNDELETED')
    for num in data[0].split():
        typ, data = mailbox.fetch(num, '(RFC822.HEADER)')
        dspam_sig = extract_dspam_signature(data[0][1])
        if dspam_sig != constants.DSPAM_NO_SIG:
            # do something
            if report_to_dspam(dspam_sig, action, user) == 0:
                move_or_delete(mailbox, num, action)

def move_or_delete(mailbox, msg, action):
    if action == constants.DSPAM_HAM_ACTION:
        # copy the message
        logging.info('Copying the message')
        mailbox.copy(msg, constants.IMAP_INBOX_FOLDER)
    # delete the original messageA
    logging.info('Deleting the message')
    mailbox.store(msg, '+FLAGS', '\\Deleted')

def extract_dspam_signature(message):
    headers = message.split(b'\r\n')
    return_value = constants.DSPAM_NO_SIG
    for hdr in headers:
        if hdr.startswith(b'X-DSPAM-Signature'):
            sig = hdr.split(b' ')
            return_value = sig[1].decode('utf-8')
    logging.info('DSPAM Signature found: %s', return_value)
    return return_value

def report_to_dspam(sig, action, user):
    s = subprocess.run([constants.DSPAM_CMD, '--source=error', '--class=' + action, '--signature=' + sig, '--user', user])
    logging.info('DSPAM being called with %s', s.args)
    logging.info('DSPAM returned: %s', s.returncode)
    return s.returncode



