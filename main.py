from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.core.window import Window
from PIL import ImageGrab
import sqlite3
import pandas as pd
import numpy as np
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton,MDRaisedButton
import os



mycon=sqlite3.connect('DBfile\\test_database.db')
cursor_ = mycon.cursor()
    
resolution = ImageGrab.grab().size
Window.size=(350,550)
#Window.size=(1050,700)
Window.top = 50
Window.left = resolution[0] /10
fixsize=(350,550)
def reZ(*args):
    Window.size=fixsize
    return True
Window.bind(on_resize=reZ)
Window.clearcolor = (0.5, 0.5, 0.5, 1)

global wdj

target=os.getcwd()+"\\images\\mat\\"
targett=os.getcwd()+"\\images\\"



class MainPage(Screen):
    pass

class Page1(Screen):
    pass

class Page2(Screen):
    pass

class Page3(Screen):
    pass

class MainApp(MDApp):

    try:
        fd = pd.read_sql_query(sql=f"""select mat from mat   """, con=mycon)
        r1=str(fd.iloc[0,0])
        wdj=r1
    except:
        pass

    def getss(self,xx,yy):
        self.sss=xx.text
        self.fff=yy.source
        
        if os.path.exists(target+ self.sss+ ".jpg"):
            eeeee=target+ self.sss+ ".jpg"
         
            yy.source=eeeee
        else:
            eeeee=targett+"avatar.jpg"
          
            yy.source=eeeee
            #self.ids.newmatricule.source=target+"avatar.jpg"
        return eeeee 
    
    def o_t_valid(self,widget,sx):
           
        try:

            df2user = pd.read_sql_query(sql="select * from tbl_user", con=mycon)
            dfm=df2user.loc[df2user['Matricule'] == int(widget.text),"Matricule"].values
            #dfp=df2user.loc[df2user['Matricule'] == int(widget.text),"Password_"].values
            dfn=df2user.loc[df2user['Matricule'] == int(widget.text),"Username"].values 
            #dfc=df2user.loc[df2user['Matricule'] == int(widget.text),"Case_"].values  

            if widget.text==str(dfm[0]):
                sql = 'UPDATE mat set  mat=?   '
                cursor_.execute(sql,[str(widget.text)])
                mycon.commit()

                #wdj_user=str(dfn[0])
                oobc="You are : "+ str(dfn[0])
                #wdj_pass=str(dfp[0])
                #matt=str(dfc[0])

                sx.text=oobc
  
   

            else:
                pass

                #wdj_user=str(dfn[0])
                #wdj_pass=str(dfp[0])

        except:  
            sx.text="This matricule does not exist "

    def clicked(self,text_,psw):
        try:
            df2user = pd.read_sql_query(sql="select * from tbl_user", con=mycon)
            dfm=df2user.loc[df2user['Matricule'] == int(text_),"Matricule"].values
            dfp=df2user.loc[df2user['Matricule'] == int(text_),"Password_"].values
            dfn=df2user.loc[df2user['Matricule'] == int(text_),"Username"].values
            dfc=df2user.loc[df2user['Matricule'] == int(text_),"Case_"].values
            if text_ ==  str(dfm[0]) and  psw ==  str(dfp[0]):
                sql = 'UPDATE mat set  mat=?   '
                cursor_.execute(sql,[text_])
                mycon.commit()
                #wdj=str(dfm[0])
                matt=str(dfc[0])
                oobc=str(dfn[0])
                self.root.current = "page1"
            
            else:
                self.dialog = MDDialog(title='Password check',
                                        text="Password does not exists !!!", size_hint=(0.8, 1),
                                        buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
                                        )
                self.dialog.open()
        
        except:
            #user_error = "Password does not exists"
            self.dialog = MDDialog(title='Password check',
                                        text="Password does not exists", size_hint=(0.8, 1),
                                        buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
                                        )
            self.dialog.open()


    def close_dialog(self, obj):
        self.dialog.dismiss()
        
    def close_application(self):
        sql = 'UPDATE mat set  mat=?   '
        cursor_.execute(sql,["00000"])
        mycon.commit()
        # closing application 
        MDApp.get_running_app().stop()
        # removing window
        Window.close()

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.icon = targett+'logo.png'
        # Charge tous les fichiers KV
        Builder.load_file("main_page.kv")
        Builder.load_file("page1.kv")
        Builder.load_file("page2.kv")
        Builder.load_file("page3.kv")
        
        # Retourne le ScreenManager avec MainPage comme écran initial
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainPage(name="main"))
        screen_manager.add_widget(Page1(name="page1"))
        screen_manager.add_widget(Page2(name="page2"))
        screen_manager.add_widget(Page3(name="page3"))
        
        return screen_manager

    def change_screen(self, screen_name):
        self.root.current = screen_name

    def switch_screen_left(self, screen_name):
        screen_manager = self.root
        # Set the transition effect and direction
        screen_manager.transition = SlideTransition(direction="left")
        screen_manager.current = screen_name
    
    def switch_screen_right(self, screen_name):
        screen_manager = self.root
        # Set the transition effect and direction
        screen_manager.transition = SlideTransition(direction="right")
        screen_manager.current = screen_name

if __name__ == "__main__":
    MainApp().run()
