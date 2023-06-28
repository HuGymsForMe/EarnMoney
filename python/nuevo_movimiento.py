from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from datetime import datetime
import mysql.connector
import configparser

Builder.load_file('./kivy/nuevo_movimiento.kv')

class NuevoMovimiento(Screen):
    def recoger_id_user(self):
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

        query = f"SELECT ID FROM usuarios WHERE gmail = %s"

        cursor.execute(query, (str(input_nickname),))
        resultado = cursor.fetchone()
        if resultado is not None:
            id_user = resultado[0]
            return id_user

    def ingress_new_movement(self):
        id_user = self.recoger_id_user()
        app = App.get_running_app()
        input_titulo = app.manager.get_screen('nuevo_movimiento').ids['input_titulo'].text
        input_descripcion = app.manager.get_screen('nuevo_movimiento').ids['input_descripcion'].text
        input_importe = app.manager.get_screen('nuevo_movimiento').ids['input_importe'].text
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        host = config['mysql']['host']
        user = config['mysql']['user']
        password = config['mysql']['password']
        dbname = config['mysql']['db']

        db = mysql.connector.connect(host = str(host), user=str(user), password=str(password), database=str(dbname))
        cursor = db.cursor()

        now = datetime.now()
        query = f"INSERT INTO MOVIMIENTOS (ID_USER, TITULO, DESCRIPCION, FECHA_MOV, VALOR_MOV) \
VALUES ({id_user}, '{str(input_titulo)}', '{str(input_descripcion)}', '{now}', {input_importe})"
        cursor.execute(query)
        db.commit()
        db.close()
        toast('Movimiento agregado con éxito')
        self.update_saldo_user(input_importe, id_user)

        #POR ÚLTIMO UN UPDATE DEL SALDO EN TABLA USUARIOS

    def update_saldo_user(self, input_importe, id_user):
        app = App.get_running_app()
        input_saldo = float((app.manager.get_screen('menu_principal').ids['saldo_user'].text)[:-1])
        input_saldo += float(input_importe)        
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        host = config['mysql']['host']
        user = config['mysql']['user']
        password = config['mysql']['password']
        dbname = config['mysql']['db']

        db = mysql.connector.connect(host = str(host), user=str(user), password=str(password), database=str(dbname))
        cursor = db.cursor()
        query = f"UPDATE USUARIOS SET SALDO = {input_saldo} WHERE ID = {id_user}"
        cursor.execute(query)
        db.commit()
        self.manager.get_screen('menu_principal').mostrar_nombre_saldo()
        self.manager.current = 'menu_principal'
        db.close()

