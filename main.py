import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.utils import platform

class TesteSomApp(App):
    def build(self):
        self.wake_lock = None
        self.player = None
        
        layout = FloatLayout()
        
        # Fundo grafite
        with layout.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.rect = Rectangle(size=(2000, 2000), pos=(0, 0))
            
        lbl_titulo = Label(
            text="a_teste_som (Modo Direto)",
            font_size='24sp',
            bold=True,
            pos_hint={'center_x': 0.5, 'y': 0.38}
        )
        layout.add_widget(lbl_titulo)
        
        self.lbl_status = Label(
            text="Status: Alarme Ativo (5 segundos)",
            font_size='18sp',
            color=(0.2, 0.8, 0.2, 1),
            pos_hint={'center_x': 0.5, 'y': 0.28}
        )
        layout.add_widget(self.lbl_status)
        
        btn_teste = Button(
            text="[ TESTAR DISPARO MANUAL ]",
            font_size='18sp',
            bold=True,
            size_hint=(0.85, 0.12),
            pos_hint={'center_x': 0.5, 'y': 0.12},
            background_normal='',
            background_color=(0.0, 0.47, 0.84, 1)
        )
        btn_teste.bind(on_press=self.disparar_manual)
        layout.add_widget(btn_teste)
        
        if platform == 'android':
            self.configurar_hardware_android()
            
        # Agenda o disparo continuo a cada 5 segundos no loop do Kivy
        Clock.schedule_interval(self.executar_pulso_alarme, 5)
            
        return layout

    def configurar_hardware_android(self):
        """Configura flags de tela acesa no bloqueio e ativa o WakeLock da CPU."""
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            WindowManager = autoclass('android.view.WindowManager$LayoutParams')
            Context = autoclass('android.content.Context')
            PowerManager = autoclass('android.os.PowerManager')
            
            # 1. Configura flags de tela para acender e sobrepor a tela de bloqueio
            # SHOW_WHEN_LOCKED (4718592) | TURN_SCREEN_ON (2097152) | KEEP_SCREEN_ON (128) | DISMISS_KEYGUARD (4194304)
            flags = 4718592 | 2097152 | 128 | 4194304
            
            activity.runOnUiThread(
                autoclass('java.lang.Runnable')(
                    lambda: activity.getWindow().addFlags(flags)
                )
            )
            
            # 2. Ativa PARTIAL_WAKE_LOCK para manter a CPU rodando na suspensão
            pm = activity.getSystemService(Context.POWER_SERVICE)
            self.wake_lock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "a_teste_som:DirectCpuLock")
            self.wake_lock.acquire()
            print("WakeLock da CPU ativado com sucesso!")
        except Exception as e:
            print(f"Erro ao configurar hardware: {e}")

    def executar_pulso_alarme(self, dt=None):
        """Dispara a vibração, som e acendimento de tela a cada 5 segundos."""
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                PowerManager = autoclass('android.os.PowerManager')
                MediaPlayer = autoclass('android.media.MediaPlayer')
                AudioAttributes = autoclass('android.media.AudioAttributes')
                
                activity = PythonActivity.mActivity
                
                # 1. Acorda o Display (Comando Acorda)
                try:
                    pm = activity.getSystemService(Context.POWER_SERVICE)
                    # SCREEN_BRIGHT_WAKE_LOCK (26) | ACQUIRE_CAUSES_WAKEUP (1) | ON_AFTER_RELEASE (10)
                    wake_screen = pm.newWakeLock(26 | 1 | 10, "a_teste_som:AcordaTelaDirect")
                    wake_screen.acquire(1500)
                except Exception as e_w:
                    print(f"Erro Wake: {e_w}")

                # 2. Vibração do Hardware
                try:
                    vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
                    if vibrator and vibrator.hasVibrator():
                        vibrator.vibrate(500)
                except Exception as e_v:
                    print(f"Erro Vib: {e_v}")

                # 3. Toca o Som sirene.mp3 no Canal de Alarme
                app_dir = activity.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"
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
                print(f"Erro no pulso de alarme: {e}")

    def disparar_manual(self, instance):
        self.executar_pulso_alarme()

if __name__ == '__main__':
    TesteSomApp().run()