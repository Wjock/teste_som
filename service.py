import os
import time
from jnius import autoclass

def iniciar_foreground():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        
        service = PythonService.mContext
        nm = service.getSystemService(Context.NOTIFICATION_SERVICE)
        
        CHANNEL_ID = "canal_teste_acorda"
        channel = NotificationChannel(
            CHANNEL_ID,
            "Teste Acorda Tela",
            NotificationManager.IMPORTANCE_HIGH
        )
        nm.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Teste de acendimento ativo")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        service.startForeground(101, builder.build())
    except Exception as e:
        print(f"Erro no Foreground: {e}")

def ciclo_acorda_toca_dormir():
    """Acorda a tela por 2 segundos, toca a sirene + vibra e depois manda a tela dormir."""
    PythonService = autoclass('org.kivy.android.PythonService')
    Context = autoclass('android.content.Context')
    PowerManager = autoclass('android.os.PowerManager')
    MediaPlayer = autoclass('android.media.MediaPlayer')
    AudioAttributes = autoclass('android.media.AudioAttributes')
    
    service = PythonService.mContext
    pm = service.getSystemService(Context.POWER_SERVICE)
    
    # 1. COMANDO ACORDAR:
    # 26 = SCREEN_BRIGHT_WAKE_LOCK | 1 = ACQUIRE_CAUSES_WAKEUP | 10 = ON_AFTER_RELEASE
    flags_acordar = 26 | 1 | 10
    screen_lock = pm.newWakeLock(flags_acordar, "a_teste_som:AcordaLock")
    
    try:
        # Pressiona o "botão virtual" para ligar a tela
        screen_lock.acquire()
        
        # 2. Vibração (Hardware)
        try:
            vibrator = service.getSystemService(Context.VIBRATOR_SERVICE)
            if vibrator and vibrator.hasVibrator():
                vibrator.vibrate(500)
        except Exception as e_vib:
            print(f"Erro vibra: {e_vib}")

        # 3. Toca o Som (Com a tela acesa pelo acquire)
        app_dir = service.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"
        if os.path.exists(app_dir):
            player = MediaPlayer()
            attr_builder = autoclass('android.media.AudioAttributes$Builder')()
            attr_builder.setUsage(AudioAttributes.USAGE_ALARM)
            attr_builder.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            
            player.setAudioAttributes(attr_builder.build())
            player.setDataSource(app_dir)
            player.prepare()
            player.start()
            
        # Mantém a tela acesa por 2 segundos para o som tocar
        time.sleep(2)
        
    except Exception as e:
        print(f"Erro no ciclo acorda/toca: {e}")
        
    finally:
        # 4. COMANDO DORMIR: Libera o lock da tela para o Android apagar
        try:
            if screen_lock.isHeld():
                screen_lock.release()
        except Exception as e_rel:
            print(f"Erro ao liberar tela: {e_rel}")

# Inicia o serviço de primeiro plano
iniciar_foreground()

# Loop contínuo com proteção try...except
while True:
    try:
        ciclo_acorda_toca_dormir()
    except Exception as e_main:
        print(f"Erro no loop principal: {e_main}")
        
    time.sleep(5)