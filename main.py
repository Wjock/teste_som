import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex, platform
from kivy.clock import Clock

class SomApp(App):
    def build(self):
        self.player = None
        self.contador = 0
        
        # Caminho do log na pasta de dados do app
        self.log_path = os.path.join(self.user_data_dir, 'suspensao_log.txt')
        
        layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=20
        )
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#1A1A24'))
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        self.label_status = Label(
            text="App Ativo - Teste de Suspensão",
            font_size='18sp',
            color=get_color_from_hex('#00E676')
        )
        
        self.label_logs = Label(
            text="Aguardando registros...",
            font_size='12sp',
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            valign='top'
        )
        self.label_logs.bind(size=self.label_logs.setter('text_size'))

        btn_tocar = Button(
            text="Tocar Som Manual",
            font_size='18sp',
            size_hint=(1, 0.15),
            background_color=get_color_from_hex('#00E676')
        )
        btn_tocar.bind(on_release=self.tocar_som)

        btn_refresh = Button(
            text="Atualizar Logs",
            font_size='16sp',
            size_hint=(1, 0.15),
            background_color=get_color_from_hex('#29B6F6')
        )
        btn_refresh.bind(on_release=self.ler_logs)

        layout.add_widget(self.label_status)
        layout.add_widget(self.label_logs)
        layout.add_widget(btn_tocar)
        layout.add_widget(btn_refresh)

        # Inicia a checagem em segundo plano a cada 10 segundos
        Clock.schedule_interval(self.rotina_segundo_plano, 10)

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gravar_log(self, mensagem):
        horario = datetime.now().strftime("%H:%M:%S")
        linha = f"[{horario}] {mensagem}\n"
        with open(self.log_path, 'a') as f:
            f.write(linha)

    def rotina_segundo_plano(self, dt):
        self.contador += 1
        self.gravar_log(f"Checagem #{self.contador}")
        
        # Na 3ª checagem (~30 seg), dispara o som automaticamente
        if self.contador == 3:
            self.gravar_log("Tentando tocar som automático...")
            self.tocar_som(None)
            
        self.ler_logs()

    def ler_logs(self, *args):
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                linhas = f.readlines()[-8:] # Pega as ultimas 8 linhas
                self.label_logs.text = "".join(linhas)

    def tocar_som(self, instance):
        nome_arquivo = "sirene.mp3"
        caminho_absoluto = os.path.abspath(nome_arquivo)

        if not os.path.exists(caminho_absoluto):
            self.label_status.text = f"Erro: {nome_arquivo} nao encontrado!"
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
                self.label_status.text = "Som disparado!"
            except Exception as e:
                self.label_status.text = f"Erro Android: {str(e)}"

if __name__ == '__main__':
    SomApp().run()
