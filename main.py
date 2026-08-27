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
        self.alarme_ativo = True
        self.event_clock = None
        
        layout = FloatLayout()
        
        # Fundo grafite
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
            text="Status: Alarme ATIVO (A cada 5s)",
            font_size='18sp',
            color=(0.2, 0.8, 0.2, 1),
            pos_hint={'center_x': 0.5, 'y': 0.28}
        )
        layout.add_widget(self.lbl_status)
        
        # Botão de Liga / Desliga Alternado (Para não sobrepor)
        self.btn_toggle = Button(
            text="[ PAUSAR ALARME ]",
            font_size='18sp',
            bold=True,
            size_hint=(0.85, 0.12),
            pos_hint={'center_x': 0.5, 'y': 0.12},
            background_normal='',
            background_color=(0.85, 0.2, 0.2, 1) # Vermelho para pausar
        )
        self.btn_toggle.bind(on_press=self.alternar_alarme)
        layout.add_widget(self.btn_toggle)
        
        if platform == 'android':
            self.configurar_hardware_android()
            
        # Agenda o disparo continuo a cada 5 segundos
        self.event_clock = Clock.schedule_interval(self.executar_pulso_alarme, 5)
            
        return layout

    def on_pause(self):
        """RETORNA TRUE: Impede a Samsung de congelar o app ao apagar a tela!"""
        return True

    def on_resume(self):
        """Re-garante que as permissões de tela fiquem ativas ao voltar."""
        if platform == 'android':
            self.configurar_hardware_android()

    def configurar_hardware_android(self):
        """Mantém a CPU ativa em suspensão via WakeLock."""
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            Context = autoclass('android.content.Context')
            PowerManager = autoclass('android.os.PowerManager')
            
            # Flags de tela sobre a tela de bloqueio
            flags = 4718592 | 2097152 | 128 | 4194304
            activity.runOnUiThread(
                autoclass('java.lang.Runnable')(
                    lambda: activity.getWindow().addFlags(flags)
                )
            )
            
            # PARTIAL_WAKE_LOCK impede a CPU de entrar em suspensão
            pm = activity.getSystemService(Context.POWER_SERVICE)
            if not self.wake_lock:
                self.wake_lock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "a_teste_som:CpuLockPermanente")
                self.wake_lock.acquire()
        except Exception as e:
            print(f"Erro ao configurar hardware: {e}")

    def executar_pulso_alarme(self, dt=None):
        if not self.alarme_ativo:
            return

        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                MediaPlayer = autoclass('android.media.MediaPlayer')
                AudioAttributes = autoclass('android.media.AudioAttributes')
                
                activity = PythonActivity.mActivity
                
                # 1. Acorda o Display por 1.5s
                try:
                    pm = activity.getSystemService(Context.POWER_SERVICE)
                    wake_screen = pm.newWakeLock(26 | 1 | 10, "a_teste_som:AcordaTelaLoop")
                    wake_screen.acquire(1500)
                except Exception as e_w:
                    print(f"Erro Wake: {e_w}")

                # 2. Vibração de Hardware
                try:
                    vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
                    if vibrator and vibrator.hasVibrator():
                        vibrator.vibrate(500)
                except Exception as e_v:
                    print(f"Erro Vib: {e_v}")

                # 3. Toca o Som sirene.mp3 no Canal de Alarme Nativo
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

    def alternar_alarme(self, instance):
        """Liga ou Desliga o ciclo sem sobrepor chamadas."""
        self.alarme_ativo = not self.alarme_ativo
        if self.alarme_ativo:
            self.lbl_status.text = "Status: Alarme ATIVO (A cada 5s)"
            self.lbl_status.color = (0.2, 0.8, 0.2, 1)
            self.btn_toggle.text = "[ PAUSAR ALARME ]"
            self.btn_toggle.background_color = (0.85, 0.2, 0.2, 1)
        else:
            self.lbl_status.text = "Status: Alarme PAUSADO"
            self.lbl_status.color = (0.8, 0.8, 0.8, 1)
            self.btn_toggle.text = "[ REINICIAR ALARME ]"
            self.btn_toggle.background_color = (0.0, 0.47, 0.84, 1)

if __name__ == '__main__':
    TesteSomApp().run()