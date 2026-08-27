import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

class TesteSomApp(App):
    def build(self):
        layout = FloatLayout()
        
        self.lbl_status = Label(
            text="Iniciando Servico Srvsom...",
            font_size='18sp',
            pos_hint={'center_x': 0.5, 'y': 0.3}
        )
        layout.add_widget(self.lbl_status)
        
        btn_iniciar = Button(
            text="Forçar Início do Serviço Srvsom",
            font_size='18sp',
            size_hint=(0.8, 0.15),
            pos_hint={'center_x': 0.5, 'y': 0.08}
        )
        btn_iniciar.bind(on_press=self.forcar_inicio_servico)
        layout.add_widget(btn_iniciar)
        
        # Dispara o serviço assim que a interface abre
        if platform == 'android':
            self.iniciar_servico_android()
            
        return layout

    def iniciar_servico_android(self):
        """Inicia o servico background no Android."""
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            
            # O p4a gera a classe com o prefixo 'Service' + nome do servico no spec (Srvsom -> ServiceSrvsom)
            service_class = autoclass('org.test.atestesom.ServiceSrvsom')
            service_class.start(activity, '')
            
            self.lbl_status.text = "Serviço Srvsom Iniciado!"
            print("Servico iniciado com sucesso via main!")
        except Exception as e:
            self.lbl_status.text = f"Erro ao iniciar servico: {e}"
            print(f"Erro ao iniciar servico: {e}")

    def forcar_inicio_servico(self, instance):
        self.iniciar_servico_android()

if __name__ == '__main__':
    TesteSomApp().run()