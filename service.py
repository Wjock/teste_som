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
        
        CHANNEL_ID = "canal_srvsom_v10"
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme de Emergencia Srvsom",
            NotificationManager.IMPORTANCE_HIGH
        )
        nm.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Serviço de Alarme Nativo Rodando")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        builder.setOngoing(True)
        
        service.startForeground(101, builder.build())
    except Exception as e:
        print(f"Erro no Foreground: {e}")

def disparar_hardware_nativo():
    """Acorda a CPU e o Display, vibra e toca a sirene."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        service = PythonService.mContext

        # 1. Acorda o Display (Comando Acorda Nativo)
        try:
            PowerManager = autoclass('android.os.PowerManager')
            pm = service.getSystemService(Context.POWER_SERVICE)
            wake_lock = pm.newWakeLock(26 | 1 | 10, "a_teste_som:AlarmWake")
            wake_lock.acquire(1500)
        except Exception as e_w:
            print(f"Erro Wake: {e_w}")

        # 2. Vibração
        try:
            vibrator = service.getSystemService(Context.VIBRATOR_SERVICE)
            if vibrator and vibrator.hasVibrator():
                vibrator.vibrate(500)
        except Exception as e_v:
            print(f"Erro Vib: {e_v}")

        # 3. Som Sirene
        try:
            MediaPlayer = autoclass('android.media.MediaPlayer')
            AudioAttributes = autoclass('android.media.AudioAttributes')
            
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
        except Exception as e_s:
            print(f"Erro Som: {e_s}")

    except Exception as e:
        print(f"Erro no disparo de hardware: {e}")

# 1. Inicia o serviço
iniciar_foreground()

# 2. Loop continuo de disparo
while True:
    try:
        disparar_hardware_nativo()
    except Exception as e_loop:
        print(f"Erro loop: {e_loop}")
        
    time.sleep(5)