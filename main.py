import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.utils import platform

class SomApp(App):
    def build(self):
        self.player = None
        
        # Layout principal
        layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=30
        )
        
        # Fundo do layout usando Hexadecimal
        with layout.canvas.before:
            Color(*get_color_from_hex('#1A1A24'))
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        # Rótulo de status do som
        self.label = Label(
            text="Pronto para tocar",
            font_size='20sp',
            color=get_color_from_hex('#FFFFFF')
        )
        
        # Botão para reproduzir o som
        btn_tocar = Button(
            text="Tocar Som",
            font_size='22sp',
            size_hint=(1, 0.3),
            background_color=get_color_from_hex('#00E676')
        )
        btn_tocar.bind(on_release=self.tocar_som)

        layout.add_widget(self.label)
        layout.add_widget(btn_tocar)
        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def tocar_som(self, instance):
        nome_arquivo = "sirene.mp3"  # Certifique-se que o arquivo existe na raiz
        caminho_absoluto = os.path.abspath(nome_arquivo)

        if not os.path.exists(caminho_absoluto):
            self.label.text = f"Erro: {nome_arquivo} nao encontrado!"
            return

        if platform == 'android':
            try:
                from jnius import autoclass
                MediaPlayer = autoclass('android.media.MediaPlayer')
                
                if self.player is not None:
                    self.player.release()

                self.player = MediaPlayer()
                self.player.setDataSource(caminho_absoluto)
                self.player.prepare()
                self.player.start()
                self.label.text = "Som tocando no Android!"
            except Exception as e:
                self.label.text = f"Erro Android: {str(e)}"
        else:
            # Fallback para execução de teste no PC
            try:
                from kivy.core.audio import SoundLoader
                sound = SoundLoader.load(caminho_absoluto)
                if sound:
                    sound.play()
                    self.label.text = "Som tocando no Desktop!"
                else:
                    self.label.text = "Falha ao carregar audio no PC"
            except Exception as e:
                self.label.text = f"Erro PC: {str(e)}"

if __name__ == '__main__':
    SomApp().run()