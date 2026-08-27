from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.utils import platform

class TesteSomApp(App):
    def build(self):
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.rect = Rectangle(size=(2000, 2000), pos=(0, 0))
            
        lbl_titulo = Label(
            text="a_teste_som (AlarmManager)",
            font_size='22sp',
            bold=True,
            pos_hint={'center_x': 0.5, 'y': 0.38}
        )
        layout.add_widget(lbl_titulo)
        
        self.lbl_status = Label(
            text="Status: Ativando AlarmManager Nativo...",
            font_size='16sp',
            color=(0.8, 0.8, 0.8, 1),
            pos_hint={'center_x': 0.5, 'y': 0.28}
        )
        layout.add_widget(self.lbl_status)
        
        btn_iniciar = Button(
            text="[ INICIAR ALARM MANAGER ]",
            font_size='18sp',
            bold=True,
            size_hint=(0.85, 0.12),
            pos_hint={'center_x': 0.5, 'y': 0.12},
            background_normal='',
            background_color=(0.0, 0.47, 0.84, 1)
        )
        btn_iniciar.bind(on_press=self.iniciar_servico_manual)
        layout.add_widget(btn_iniciar)
        
        if platform == 'android':
            self.iniciar_servico_android()
            
        return layout

    def iniciar_servico_android(self):
        try:
            from android import mActivity
            from jnius import autoclass
            
            service_name = 'Srvsom'
            package_name = 'org.test.atestesom'
            
            service_class = autoclass(f'{package_name}.Service{service_name}')
            service_class.start(mActivity, '')
            
            self.lbl_status.text = "Status: AlarmManager Agendado no Kernel!"
            self.lbl_status.color = (0.2, 0.8, 0.2, 1)
        except Exception as e:
            self.lbl_status.text = f"Erro ao iniciar: {e}"
            self.lbl_status.color = (0.9, 0.2, 0.2, 1)

    def iniciar_servico_manual(self, instance):
        self.iniciar_servico_android()

if __name__ == '__main__':
    TesteSomApp().run()