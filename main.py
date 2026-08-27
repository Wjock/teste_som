import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.utils import platform

class TesteSomApp(App):
    def build(self):
        layout = FloatLayout()
        
        btn_tocar = Button(
            text="Tocar Som Manual",
            font_size='20sp',
            size_hint=(0.8, 0.15),
            pos_hint={'center_x': 0.5, 'y': 0.08}
        )
        btn_tocar.bind(on_press=self.tocar_som_manual)
        layout.add_widget(btn_tocar)
        
        if platform == 'android':
            self.configurar_flags_tela_bloqueio()
            self.iniciar_servico_android()
            
        return layout

    def configurar_flags_tela_bloqueio(self):
        """Ativa as flags nativas do Android para acender a tela sobre o bloqueio."""
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            WindowManager = autoclass('android.view.WindowManager$LayoutParams')
            
            # Flags para acordar o display e mostrar sobre a tela de bloqueio
            # FLAG_SHOW_WHEN_LOCKED (4718592) | FLAG_TURN_SCREEN_ON (2097152) | FLAG_KEEP_SCREEN_ON (128)
            flags = (
                WindowManager.FLAG_SHOW_WHEN_LOCKED |
                WindowManager.FLAG_TURN_SCREEN_ON |
                WindowManager.FLAG_KEEP_SCREEN_ON |
                WindowManager.FLAG_DISMISS_KEYGUARD
            )
            
            activity.runOnUiThread(
                autoclass('java.lang.Runnable')(
                    lambda: activity.getWindow().addFlags(flags)
                )
            )
        except Exception as e:
            print(f"Erro ao configurar flags da janela: {e}")

    def on_new_intent(self, intent):
        """Chamado quando o serviço envia um disparo para a Activity acesa."""
        if platform == 'android':
            self.executar_alarme_completo()

    def iniciar_servico_android(self):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            
            service = autoclass('org.test.atestesom.ServiceSrvsom')
            service.start(activity, '')
        except Exception as e:
            print(f"Erro ao iniciar servico: {e}")

    def executar_alarme_completo(self):
        """Executa o som e a vibração com a tela e a GPU ativas."""
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                MediaPlayer = autoclass('android.media.MediaPlayer')
                AudioAttributes = autoclass('android.media.AudioAttributes')
                
                activity = PythonActivity.mActivity
                app_dir = activity.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"

                # 1. Vibração via hardware
                try:
                    vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
                    if vibrator and vibrator.hasVibrator():
                        vibrator.vibrate(500)
                except Exception as e_vib:
                    print(f"Erro vibra main: {e_vib}")

                # 2. Som via MediaPlayer de Alarme
                if os.path.exists(app_dir):
                    player = MediaPlayer()
                    attr_builder = autoclass('android.media.AudioAttributes$Builder')()
                    attr_builder.setUsage(AudioAttributes.USAGE_ALARM)
                    attr_builder.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                    
                    player.setAudioAttributes(attr_builder.build())
                    player.setDataSource(app_dir)
                    player.prepare()
                    player.start()
            except Exception as e:
                print(f"Erro ao tocar alarme no main: {e}")

    def tocar_som_manual(self, instance):
        self.executar_alarme_completo()

if __name__ == '__main__':
    TesteSomApp().run()