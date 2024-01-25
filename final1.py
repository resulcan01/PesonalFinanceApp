from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle

user_database = {
    "user": "password"
}

class GirisEkrani(BoxLayout):
    def __init__(self, app, **kwargs):
        super(GirisEkrani, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.spacing = 10

        self.kullanici_adi_input = TextInput(hint_text='Kullanıcı Adı', font_size=20)
        self.sifre_input = TextInput(hint_text='Şifre', password=True, font_size=20)

        self.giris_dugmesi = Button(text='Giriş', font_size=20, background_color=(0.1, 0.7, 0.3, 1))
        self.giris_dugmesi.bind(on_press=self.giris)

        self.kayit_ekrani_dugmesi = Button(text='Kayıt Ol', font_size=20, background_color=(0.5, 0.5, 0.5, 0.5))
        self.kayit_ekrani_dugmesi.bind(on_press=self.kayit_ekrani)

        input_layout = BoxLayout(orientation='vertical', spacing=10)
        input_layout.add_widget(self.kullanici_adi_input)
        input_layout.add_widget(self.sifre_input)
        input_layout.add_widget(self.giris_dugmesi)
        input_layout.add_widget(self.kayit_ekrani_dugmesi)

        self.add_widget(input_layout)

    def giris(self, instance):
        username = self.kullanici_adi_input.text.strip()
        password = self.sifre_input.text.strip()

        if username in user_database and user_database[username] == password:
            print(f"Giriş yapılan kullanıcı adı: {username}, Şifre: {password}")
            self.app.change_screen("gelir_gider")
        else:
            print("Hatalı kullanıcı adı veya şifre!")

    def kayit_ekrani(self, instance):
        self.app.change_screen("kayit")


class KayitEkrani(BoxLayout):
    def __init__(self, app, **kwargs):
        super(KayitEkrani, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.spacing = 10

        self.kullanici_adi_input = TextInput(hint_text='Kullanıcı Adı', font_size=20)
        self.sifre_input = TextInput(hint_text='Şifre', password=True, font_size=20)

        self.kayit_dugmesi = Button(text='Kayıt Ol', font_size=20, background_color=(0.1, 0.7, 0.3, 1))
        self.kayit_dugmesi.bind(on_press=self.kayit)

        self.giris_ekrani_dugmesi = Button(text='Giriş Ekranına Dön', font_size=20, background_color=(0.1, 0.7, 0.3, 1))
        self.giris_ekrani_dugmesi.bind(on_press=self.giris_ekrani)

        input_layout = BoxLayout(orientation='vertical', spacing=10)
        input_layout.add_widget(self.kullanici_adi_input)
        input_layout.add_widget(self.sifre_input)
        input_layout.add_widget(self.kayit_dugmesi)
        input_layout.add_widget(self.giris_ekrani_dugmesi)

        self.add_widget(input_layout)

    def kayit(self, instance):
        new_username = self.kullanici_adi_input.text.strip()
        new_password = self.sifre_input.text.strip()

        if new_username not in user_database:
            user_database[new_username] = new_password
            print(f"Yeni Kullanıcı Kaydı: Kullanıcı adı: {new_username}, Şifre: {new_password}")
        else:
            print("Bu kullanıcı zaten var!")

        self.app.change_screen("giris")

    def giris_ekrani(self, instance):
        self.app.change_screen("giris")


class GelirGiderUygulamasi(BoxLayout):
    def __init__(self, **kwargs):
        super(GelirGiderUygulamasi, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Gri rengi (RGB formatında)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
        

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

        self.gelir_listesi = []
        self.gider_listesi = []

        self.add_widget(Label(text='Gelir-Gider Uygulaması', font_size=25))

        gelir_layout = BoxLayout(orientation='horizontal', spacing=10)
        gelir_layout.add_widget(Label(text='Gelir:', font_size=20))
        self.gelir_input = TextInput(multiline=False, font_size=20)
        gelir_layout.add_widget(self.gelir_input)
        self.add_widget(gelir_layout)
        
        gider_layout = BoxLayout(orientation='horizontal', spacing=10)
        gider_layout.add_widget(Label(text='Gider:', font_size=20))
        self.gider_input = TextInput(multiline=False, font_size=20)
        gider_layout.add_widget(self.gider_input)
        self.add_widget(gider_layout)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        ekle_dugme = Button(text='Ekle', font_size=20, background_color=(0.1, 0.7, 0.3, 1))
        ekle_dugme.bind(on_press=self.ekle)
        sil_dugme = Button(text='Sil', font_size=20, background_color=(0.9, 0.1, 0.3, 1))
        sil_dugme.bind(on_press=self.sil)
        button_layout.add_widget(ekle_dugme)
        button_layout.add_widget(sil_dugme)
        self.add_widget(button_layout)

        self.toplam_gelir_label = Label(text='Toplam Gelir: 0', font_size=20)
        self.toplam_gider_label = Label(text='Toplam Gider: 0', font_size=20)
        self.bakiye_label = Label(text='Bakiye: 0', font_size=20)

        self.add_widget(self.toplam_gelir_label)
        self.add_widget(self.toplam_gider_label)
        self.add_widget(self.bakiye_label)

    def ekle(self, instance):
        try:
            gelir = float(self.gelir_input.text) if self.gelir_input.text else 0
            gider = float(self.gider_input.text) if self.gider_input.text else 0
        except ValueError:
            print("Hata: Geçerli bir sayı giriniz.")
            return

        self.gelir_listesi.append(gelir)
        self.gider_listesi.append(gider)

        self.guncelle_etiketler()

        self.gelir_input.text = ''
        self.gider_input.text = ''

    def sil(self, instance):
        if self.gelir_listesi:
            self.gelir_listesi.pop()
        if self.gider_listesi:
            self.gider_listesi.pop()

        self.guncelle_etiketler()

    def guncelle_etiketler(self):
        toplam_gelir = sum(self.gelir_listesi)
        toplam_gider = sum(self.gider_listesi)
        bakiye = toplam_gelir - toplam_gider

        self.toplam_gelir_label.text = f'Toplam Gelir: {toplam_gelir}'
        self.toplam_gider_label.text = f'Toplam Gider: {toplam_gider}'
        self.bakiye_label.text = f'Bakiye: {bakiye}'


class GelirGiderUygulamasiApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.giris_ekrani = GirisEkrani(self)
        screen = Screen(name='giris')
        screen.add_widget(self.giris_ekrani)
        self.screen_manager.add_widget(screen)

        self.kayit_ekrani = KayitEkrani(self)
        screen = Screen(name='kayit')
        screen.add_widget(self.kayit_ekrani)
        self.screen_manager.add_widget(screen)

        self.gelir_gider_ekrani = GelirGiderUygulamasi()
        screen = Screen(name='gelir_gider')
        screen.add_widget(self.gelir_gider_ekrani)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def change_screen(self, screen_name):
        self.screen_manager.current = screen_name


if __name__ == '__main__':
    GelirGiderUygulamasiApp().run()
