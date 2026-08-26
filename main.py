import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.utils import platform

class TesteSomApp(App):
    def build(self):
        layout = FloatLayout()
        
        # Botão no rodapé
        btn_tocar = Button(
            text="Tocar Som Manual",
            font_size='20sp',
            size_hint=(0.8, 0.15),
            pos_hint={'center_x': 0.5, 'y': 0.08}
        )
        btn_tocar.bind(on_press=self.tocar_som_manual)
        layout.add_widget(btn_tocar)
        
        # Inicia o serviço em segundo plano no Android
        if platform == 'android':
            self.iniciar_servico_android()
            
        return layout

    def iniciar_servico_android(self):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            
            # Serviço registrado no buildozer.spec
            service = autoclass('org.test.atestesom.ServiceSrvsom')
            service.start(activity, '')
        except Exception as e:
            print(f"Erro ao iniciar servico: {e}")

    def tocar_som_manual(self, instance):
        if platform == 'android':
            try:
                from jnius import autoclass
                MediaPlayer = autoclass('android.media.MediaPlayer')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                activity = PythonActivity.mActivity
                app_dir = activity.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"

                if os.path.exists(app_dir):
                    player = MediaPlayer()
                    player.setDataSource(app_dir)
                    player.prepare()
                    player.start()
            except Exception as e:
                print(f"Erro ao tocar mp3 manual: {e}")

if __name__ == '__main__':
    TesteSomApp().run()