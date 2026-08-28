import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.utils import platform

class TesteSomApp(App):
    def build(self):
        layout = FloatLayout()
        
        # Fundo grafite padronizado
        with layout.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.rect = Rectangle(size=(2000, 2000), pos=(0, 0))
            
        lbl_titulo = Label(
            text="a_teste_som",
            font_size='24sp',
            bold=True,
            pos_hint={'center_x': 0.5, 'y': 0.38}
        )
        layout.add_widget(lbl_titulo)
        
        self.lbl_status = Label(
            text="Status: Sistema Pronto",
            font_size='16sp',
            color=(0.8, 0.8, 0.8, 1),
            pos_hint={'center_x': 0.5, 'y': 0.28}
        )
        layout.add_widget(self.lbl_status)
        
        self.btn_iniciar = Button(
            text="[ INICIAR SERVIÇO DE ALARME ]",
            font_size='18sp',
            bold=True,
            size_hint=(0.85, 0.12),
            pos_hint={'center_x': 0.5, 'y': 0.12},
            background_normal='',
            background_color=(0.0, 0.47, 0.84, 1)
        )
        self.btn_iniciar.bind(on_press=self.iniciar_servico_manual)
        layout.add_widget(self.btn_iniciar)
        
        # Dispara o serviço ao abrir, se estiver no Android
        if platform == 'android':
            self.iniciar_servico_android()
            
        return layout

    def iniciar_servico_android(self):
        """Inicia o serviço Android utilizando a ponte padrão do Kivy."""
        try:
            from android import mActivity
            from jnius import autoclass
            
            # Chama o serviço registrado no Buildozer (Srvsom)
            service_class = autoclass('org.test.atestesom.ServiceSrvsom')
            service_class.start(mActivity, '')
            
            self.lbl_status.text = "Status: Serviço Iniciado!"
            self.lbl_status.color = (0.2, 0.8, 0.2, 1)
            self.btn_iniciar.background_color = (0.1, 0.6, 0.2, 1)
        except Exception as e:
            self.lbl_status.text = f"Status: Aguardando toque no botão"
            print(f"Aviso ao iniciar servico: {e}")

    def iniciar_servico_manual(self, instance):
        self.iniciar_servico_android()

if __name__ == '__main__':
    TesteSomApp().run()