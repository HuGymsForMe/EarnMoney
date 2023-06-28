from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import mysql.connector
import configparser

Builder.load_file('./kivy/menu_principal.kv')

class MenuPrincipal(Screen):
    def mostrar_nombre_saldo(self):
        app = App.get_running_app()
        input_nickname = app.manager.get_screen('login').ids['input_nickname'].text
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        host = config['mysql']['host']
        user = config['mysql']['user']
        password = config['mysql']['password']
        dbname = config['mysql']['db']

        db = mysql.connector.connect(host = str(host), user=str(user), password=str(password), database=str(dbname))
        cursor = db.cursor()

        query = f"SELECT saldo FROM usuarios WHERE gmail = %s"

        cursor.execute(query, (str(input_nickname),))
        resultado = cursor.fetchone()
        if resultado is not None:
            saldo = resultado[0]
            menu_principal = app.manager.get_screen('menu_principal')
            menu_principal.ids.label_nickname.text = input_nickname
            menu_principal.ids.saldo_user.text = f"{str(saldo)}€"
            print(saldo)
