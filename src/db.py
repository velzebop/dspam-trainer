import mysql.connector
import constants


def get_users_from_database():
    mydb = mysql.connector.connect(host=constants.DB_HOST, user=constants.DB_USER,
                                   passwd=constants.DB_PASS, database=constants.DB_DATABASE)

    mycursor = mydb.cursor()

    mycursor.execute("select username from mailbox where active = 1")

    return mycursor.fetchall()
