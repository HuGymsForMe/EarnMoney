from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from datetime import datetime
import mysql.connector
import configparser

Builder.load_file('./kivy/registrarse.kv')

class Registrarse(Screen):
    def insert(self):
        app = App.get_running_app()
        input_nickname = app.manager.get_screen('registrarse').ids['input_nickname'].text
        input_password = app.manager.get_screen('registrarse').ids['input_password'].text
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        host = config['mysql']['host']
        user = config['mysql']['user']
        password = config['mysql']['password']
        dbname = config['mysql']['db']

        db = mysql.connector.connect(host = str(host), user=str(user), password=str(password), database=str(dbname))
        cursor = db.cursor()

        query = f"SELECT COUNT(*) FROM USUARIOS WHERE GMAIL = '{str(input_nickname)}'"
        cursor.execute(query)
        data = cursor.fetchone()
        count = data[0]

        if 5 < len(input_nickname) < 11:
            if count == 0 and input_nickname != '' and input_password != '':
                now = datetime.now()
                query = f"INSERT INTO USUARIOS (GMAIL, PASSWORD, LAST_LOGIN) VALUES ('{str(input_nickname)}', '{str(input_password)}', '{now}')"
                cursor.execute(query)
                db.commit()
                toast('Usuario creado')
                screen_manager = self.manager
                screen_manager.current = 'login'
            elif count > 0:
                toast('Este usuario ya se encuentra en el sistema')
            elif input_nickname == '' or input_password == '':
                toast('Debes rellenar todos los campos')
            db.close()
        else:
            toast('  El nombre de usuario debe \ntener entre 6 y 10 caracteres')

        