from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class TesteSomApp(App):
    def build(self):
        # Layout limpo sem textos explicativos
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Botão único central
        btn_tocar = Button(
            text="Tocar Som Manual",
            font_size='20sp',
            size_hint=(1, 0.3)
        )
        btn_tocar.bind(on_press=self.tocar_som_manual)
        
        layout.add_widget(btn_tocar)
        
        # Inicia o loop de 5 segundos
        Clock.schedule_interval(self.loop_suspensao, 5)
        
        return layout

    def tocar_som_manual(self, instance):
        self.reproduzir_sirene()

    def loop_suspensao(self, dt):
        self.reproduzir_sirene()

    def reproduzir_sirene(self):
        # Carrega e toca o áudio alarme.wav (ou alarme.mp3)
        sound = SoundLoader.load('alarme.wav')
        if sound:
            sound.play()

if __name__ == '__main__':
    TesteSomApp().run()