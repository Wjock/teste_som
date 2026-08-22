import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader

kivy.require('2.3.0')

class TesteSomApp(App):
    def build(self):
        # Tenta carregar o arquivo ogg
        self.sound = SoundLoader.load('sirene.ogg')
        
        self.btn = Button(
            text="TOCAR SIRENE",
            background_color=(0.8, 0.1, 0.1, 1),
            font_size=24
        )
        self.btn.bind(on_press=self.tocar)
        return self.btn

    def tocar(self, instance):
        if self.sound:
            self.btn.text = "SOM CARREGADO! TOCANDO..."
            self.sound.volume = 1.0  # Força volume máximo
            if self.sound.state == 'play':
                self.sound.stop()
            self.sound.play()
        else:
            self.btn.text = "ERRO: OGG NAO ENCONTRADO"

if __name__ == '__main__':
    TesteSomApp().run()
