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
        
        # Fundo escuro elegante para contrastar os elementos
        with layout.canvas.before:
            Color(0.12, 0.12, 0.12, 1)  # Grafite escuro
            self.rect = Rectangle(size=(2000, 2000), pos=(0, 0))
            
        # Título do Aplicativo
        lbl_titulo = Label(
            text="a_teste_som",
            font_size='28sp',
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'y': 0.38}
        )
        layout.add_widget(lbl_titulo)
        
        # Texto de Status do Serviço
        self.lbl_status = Label(
            text="Status: Aguardando toque no botão...",
            font_size='16sp',
            color=(0.8, 0.8, 0.8, 1),
            pos_hint={'center_x': 0.5, 'y': 0.28}
        )
        layout.add_widget(self.lbl_status)
        
        # Botão ESTILIZADO com destaque visual (Azul/Verde de Destaque)
        self.btn_iniciar = Button(
            text="[ INICIAR SERVIÇO SRVSOM ]",
            font_size='18sp',
            bold=True,
            size_hint=(0.85, 0.12),
            pos_hint={'center_x': 0.5, 'y': 0.12},
            background_normal='',  # Remove a textura cinza padrão do Kivy
            background_color=(0.0, 0.47, 0.84, 1)  # Azul destacado
        )
        self.btn_iniciar.bind(on_press=self.iniciar_servico_manual)
        layout.add_widget(self.btn_iniciar)
        
        # Tenta disparar o serviço automaticamente ao abrir
        if platform == 'android':
            self.iniciar_servico_android()
            
        return layout

    def iniciar_servico_android(self):
        """Inicia o serviço nativo no Android."""
        try:
            from android import mActivity
            from jnius import autoclass
            
            service_name = 'Srvsom'
            package_name = 'org.test.atestesom'
            
            # Chama a classe do serviço gerada pelo p4a
            service_class = autoclass(f'{package_name}.Service{service_name}')
            service_class.start(mActivity, '')
            
            self.lbl_status.text = "Status: Serviço Srvsom em Execução!"
            self.lbl_status.color = (0.2, 0.8, 0.2, 1)  # Verde
            self.btn_iniciar.background_color = (0.1, 0.6, 0.2, 1)  # Fica verde ao ativar
            self.btn_iniciar.text = "SERVIÇO ATIVO (REINICIAR)"
            print("Serviço Srvsom iniciado com sucesso!")
        except Exception as e:
            self.lbl_status.text = f"Erro no serviço: {e}"
            self.lbl_status.color = (0.9, 0.2, 0.2, 1)  # Vermelho
            print(f"Erro no serviço: {e}")

    def iniciar_servico_manual(self, instance):
        self.iniciar_servico_android()

if __name__ == '__main__':
    TesteSomApp().run()