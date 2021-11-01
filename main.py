from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from mcrcon import MCRcon as r
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.properties import StringProperty
import sys
import os

class MainWindow(BoxLayout):
    
    connection_refused = True
    while connection_refused:
        ip = str(input('enter ip or hostname of the server:\n>'))   

        try:                   
            port = int(input('enter the server port (default: 25575):\n>'))
            if port not in range(0,65535+1):
                raise ValueError          
        except ValueError:
            print('invalid value! using default.')
            port = 25575
                    
        pw = str(input('enter server password:\n>'))

        try:
            with r (host=ip, port=port, password=pw) as mcr: 
                mcr.command('list')
                connection_refused = False
        except ConnectionRefusedError:
            print('connection refused, try again!')
            connection_refused = True

    player_count = StringProperty('')
    selected_player = StringProperty('')
    lives_to_set = StringProperty('')   

    def player_count_refresh(self):        
        with r (host=self.ip, port=self.port, password=self.pw) as mcr:
            self.player_count = mcr.command('list')
    
    def selected_player_submit(self):
        self.selected_player = str(self.ids.textinput_selected_player.text) 
                
    def player_heal(self):        
        with r (host=self.ip, port=self.port, password=self.pw) as mcr:
            self.player_count = mcr.command('effect give '+self.selected_player+' minecraft:instant_health 1 50')
                    
    def player_tp_to_spawn(self):
        with r (host=self.ip, port=self.port, password=self.pw) as mcr:
            self.player_count = mcr.command('tp '+self.selected_player+' 0 ~ 0')
        
    def player_set_lives(self):
        self.lives_to_set = str(self.ids.slider_player_lives_to_set.value)
        with r (host=self.ip, port=self.port, password=self.pw) as mcr:
            self.player_count = mcr.command('setlives '+self.selected_player+' '+self.lives_to_set)
        
    def player_revoke_progress(self):  
        with r (host=self.ip, port=self.port, password=self.pw) as mcr:
            self.player_count = mcr.command('advancement revoke '+self.selected_player+' everything')        

    def player_give_op(self):
        with r (host=self.ip, port=self.port, password=self.pw) as mcr:
            self.player_count = mcr.command('op '+self.selected_player) 

    def player_revoke_op(self):
        with r (host=self.ip, port=self.port, password=self.pw) as mcr:
            self.player_count = mcr.command('deop '+self.selected_player) 
    
    def player_kick(self):
        with r (host=self.ip, port=self.port, password=self.pw) as mcr:
            self.player_count = mcr.command('kick '+self.selected_player) 
    
class PyMinecraftContolPanel(App):
    def build(self):
        Builder.load_file('pmcp.kv')        
        return MainWindow()

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))

    PyMinecraftContolPanel().run()