import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex, platform

class SomApp(App):
    def build(self):
        self.player = None
        
        layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=30
        )
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#1A1A24'))
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        self.label = Label(
            text="Iniciando...",
            font_size='18sp',
            color=get_color_from_hex('#FFFFFF')
        )
        
        btn_tocar = Button(
            text="Tocar Som Manual",
            font_size='22sp',
            size_hint=(1, 0.3),
            background_color=get_color_from_hex('#00E676')
        )
        btn_tocar.bind(on_release=self.tocar_som_manual)

        layout.add_widget(self.label)
        layout.add_widget(btn_tocar)

        if platform == 'android':
            self.iniciar_servico()

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def iniciar_servico(self):
        try:
            from jnius import autoclass
            PythonService = autoclass('org.kivy.android.PythonService')
            # Classe do serviço criada pelo Buildozer (org.test.testesom.ServiceSrvsom)
            service = autoclass('org.test.testesom.ServiceSrvsom')
            service.start(PythonService.mContext, '')
            self.label.text = "Serviço ativo! Pode apagar a tela."
        except Exception as e:
            self.label.text = f"Erro ao iniciar serviço: {str(e)}"

    def tocar_som_manual(self, instance):
        nome_arquivo = "sirene.mp3"
        caminho_absoluto = os.path.abspath(nome_arquivo)

        if os.path.exists(caminho_absoluto) and platform == 'android':
            try:
                from jnius import autoclass
                MediaPlayer = autoclass('android.media.MediaPlayer')
                if self.player is not None:
                    self.player.release()
                self.player = MediaPlayer()
                self.player.setDataSource(caminho_absoluto)
                self.player.prepare()
                self.player.start()
                self.label.text = "Som manual disparado!"
            except Exception as e:
                self.label.text = f"Erro: {str(e)}"

if __name__ == '__main__':
    SomApp().run()