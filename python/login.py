from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from datetime import datetime
import mysql.connector
import configparser

Builder.load_file('./kivy/login.kv')

class Login(Screen):
    def ingress(self):
        app = App.get_running_app()
        input_nickname = app.manager.get_screen('login').ids['input_nickname'].text
        input_password = app.manager.get_screen('login').ids['input_password'].text
        config = configparser.ConfigParser()
        config.read('./sql/config.ini')

        host = config['mysql']['host']
        user = config['mysql']['user']
        password = config['mysql']['password']
        dbname = config['mysql']['db']

        db = mysql.connector.connect(host = str(host), user=str(user), password=str(password), database=str(dbname))
        cursor = db.cursor()

        query = f"SELECT COUNT(*) FROM USUARIOS WHERE GMAIL = '{str(input_nickname)}' AND PASSWORD = '{str(input_password)}'"
        cursor.execute(query)
        data = cursor.fetchone()
        count = data[0]

        if count == 0:
            toast('Contrasenia inválida!!!')
        else:
            toast('Perfecto, puedes acceder al sistema')
            now = datetime.now()
            query = f"UPDATE USUARIOS SET LAST_LOGIN = '{now}' WHERE GMAIL = '{str(input_nickname)}' AND PASSWORD = '{str(input_password)}'"
            cursor.execute(query)
            db.commit()
        db.close()