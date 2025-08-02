from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.core.window import Window
from PIL import ImageGrab
import sqlite3
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRaisedButton
import os

mycon = sqlite3.connect('DBfile\\test_database.db')
cursor_ = mycon.cursor()

resolution = ImageGrab.grab().size
Window.size = (350, 550)
Window.top = 50
Window.left = resolution[0] / 10
fixsize = (350, 550)

def reZ(*args):
    Window.size = fixsize
    return True

Window.bind(on_resize=reZ)
Window.clearcolor = (0.5, 0.5, 0.5, 1)

global wdj

target = os.getcwd() + "\\images\\mat\\"
targett = os.getcwd() + "\\images\\"

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
        cursor_.execute("SELECT mat FROM mat")
        r1 = cursor_.fetchone()
        if r1:
            wdj = str(r1[0])
    except:
        pass

    def getss(self, xx, yy):
        self.sss = xx.text
        self.fff = yy.source

        if os.path.exists(target + self.sss + ".jpg"):
            eeeee = target + self.sss + ".jpg"
            yy.source = eeeee
        else:
            eeeee = targett + "avatar.jpg"
            yy.source = eeeee

        return eeeee

    def o_t_valid(self, widget, sx):
        try:
            cursor_.execute("SELECT Matricule, Username FROM tbl_user WHERE Matricule = ?", (widget.text,))
            result = cursor_.fetchone()
            if result:
                cursor_.execute('UPDATE mat SET mat=?', (str(widget.text),))
                mycon.commit()
                oobc = "You are : " + str(result[1])
                sx.text = oobc
            else:
                pass
        except:
            sx.text = "This matricule does not exist"

    def clicked(self, text_, psw):
        try:
            cursor_.execute("SELECT Matricule, Password_, Username, Case_ FROM tbl_user WHERE Matricule = ?", (text_,))
            result = cursor_.fetchone()
            if result and text_ == str(result[0]) and psw == str(result[1]):
                cursor_.execute('UPDATE mat SET mat=?', (text_,))
                mycon.commit()
                self.root.current = "page1"
            else:
                self.dialog = MDDialog(
                    title='Password check',
                    text="Password does not exist !!!", size_hint=(0.8, 1),
                    buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
                )
                self.dialog.open()
        except:
            self.dialog = MDDialog(
                title='Password check',
                text="Password does not exist", size_hint=(0.8, 1),
                buttons=[MDFlatButton(text='Close', on_release=self.close_dialog)]
            )
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def close_application(self):
        cursor_.execute('UPDATE mat SET mat=?', ("00000",))
        mycon.commit()
        MDApp.get_running_app().stop()
        Window.close()

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.icon = targett + 'R.png'
        Builder.load_file("main_page.kv")
        Builder.load_file("page1.kv")
        Builder.load_file("page2.kv")
        Builder.load_file("page3.kv")

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
        screen_manager.transition = SlideTransition(direction="left")
        screen_manager.current = screen_name

    def switch_screen_right(self, screen_name):
        screen_manager = self.root
        screen_manager.transition = SlideTransition(direction="right")
        screen_manager.current = screen_name

if __name__ == "__main__":
    MainApp().run()
