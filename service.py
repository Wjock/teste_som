
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
        
        CHANNEL_ID = "canal_teste_acorda_v2"
        channel = NotificationChannel(
            CHANNEL_ID,
            "Servico Srvsom Ativo",
            NotificationManager.IMPORTANCE_HIGH
        )
        nm.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Serviço Srvsom rodando em segundo plano")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        service.startForeground(101, builder.build())
    except Exception as e:
        print(f"Erro no Foreground: {e}")

def ciclo_acorda_toca_dormir():
    PythonService = autoclass('org.kivy.android.PythonService')
    Context = autoclass('android.content.Context')
    PowerManager = autoclass('android.os.PowerManager')
    MediaPlayer = autoclass('android.media.MediaPlayer')
    AudioAttributes = autoclass('android.media.AudioAttributes')
    
    service = PythonService.mContext
    pm = service.getSystemService(Context.POWER_SERVICE)
    
    # 26 = SCREEN_BRIGHT_WAKE_LOCK | 1 = ACQUIRE_CAUSES_WAKEUP | 10 = ON_AFTER_RELEASE
    flags_acordar = 26 | 1 | 10
    screen_lock = pm.newWakeLock(flags_acordar, "a_teste_som:AcordarTelaLock")
    
    try:
        # 1. ACORDA A TELA
        screen_lock.acquire()
        
        # 2. VIBRAÇÂO
        try:
            vibrator = service.getSystemService(Context.VIBRATOR_SERVICE)
            if vibrator and vibrator.hasVibrator():
                vibrator.vibrate(500)
        except Exception as e_vib:
            print(f"Erro vibra: {e_vib}")

        # 3. TOCAR SOM
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
            
        time.sleep(2)  # Mantém a luz por 2 segundos
        
    except Exception as e:
        print(f"Erro no ciclo: {e}")
        
    finally:
        # 4. MANDE DORMIR
        try:
            if screen_lock.isHeld():
                screen_lock.release()
        except Exception as e_rel:
            print(f"Erro ao liberar tela: {e_rel}")

# Inicia a notificação no topo
iniciar_foreground()

# Loop contínuo a cada 5 segundos
while True:
    try:
        ciclo_acorda_toca_dormir()
    except Exception as e_loop:
        print(f"Erro no loop: {e_loop}")
        
    time.sleep(5)