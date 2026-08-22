import os
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader

kivy.require('2.3.0')

class TesteSomApp(App):
    def build(self):
        # Localiza o arquivo de forma precisa dentro do pacote instalado no Android
        caminho_som = os.path.join(os.path.dirname(__file__), 'sirene.ogg')
        self.sound = SoundLoader.load(caminho_som)
        
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
            self.sound.volume = 1.0
            if self.sound.state == 'play':
                self.sound.stop()
            self.sound.play()
        else:
            self.btn.text = "ERRO: OGG NAO ENCONTRADO"

if __name__ == '__main__':
    TesteSomApp().run()
