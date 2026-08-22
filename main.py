import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader

kivy.require('2.3.0')

class TesteSomApp(App):
    def build(self):
        # Pré-carrega o áudio na inicialização para não travar a tela ao clicar
        self.sound = SoundLoader.load('sirene.ogg')
        
        btn = Button(
            text="TOCAR SIRENE",
            background_color=(0.8, 0.1, 0.1, 1),
            font_size=24
        )
        btn.bind(on_press=self.tocar)
        return btn

    def tocar(self, instance):
        if self.sound:
            if self.sound.state == 'play':
                self.sound.stop()
            self.sound.play()

if __name__ == '__main__':
    TesteSomApp().run()
