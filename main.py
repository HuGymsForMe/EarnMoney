from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
import kivy
from python.login import Login
from python.registrarse import Registrarse

kivy.require('1.11.1')
Window.size = (350, 500)

class LoginApp(MDApp):
    def build(self):
        self.manager = ScreenManager(transition = SlideTransition())
        self.manager.add_widget(Builder.load_file("kivy/pantalla_inicio.kv"))
        self.manager.add_widget(Login(name='login'))
        self.manager.add_widget(Registrarse(name='registrarse'))
        return self.manager
    
    def on_start(self):
        Clock.schedule_once(self.login, 3)

    def login(self, *args):
        self.manager.current = "login"

if __name__ == '__main__':
    LoginApp().run()