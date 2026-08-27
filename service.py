import os
import time
from jnius import autoclass

def iniciar_foreground_notification():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mContext
        
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        Context = autoclass('android.content.Context')
        
        CHANNEL_ID = "canal_alarme_teste"
        
        notification_manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme Ativo",
            NotificationManager.IMPORTANCE_LOW
        )
        notification_manager.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Alarme em segundo plano ativo")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        notification = builder.build()
        service.startForeground(101, notification)
    except Exception as e:
        print(f"Erro ao iniciar Foreground Notification: {e}")

def adquirir_wake_lock():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        
        service = PythonService.mContext
        pm = service.getSystemService(Context.POWER_SERVICE)
        wake_lock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "a_teste_som:WakeLock")
        wake_lock.acquire()
        return wake_lock
    except Exception as e:
        print(f"Erro WakeLock no Service: {e}")
        return None

def vibrar_dispositivo(duracao_ms=500):
    """Aciona diretamente o motor de vibração do hardware do celular."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        service = PythonService.mContext
        
        vibrator = service.getSystemService(Context.VIBRATOR_SERVICE)
        if vibrator and vibrator.hasVibrator():
            vibrator.vibrate(duracao_ms)
    except Exception as e:
        print(f"Erro ao vibrar: {e}")

def tocar_som():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        AudioManager = autoclass('android.media.AudioManager')
        
        service = PythonService.mContext
        
        audio_manager = service.getSystemService(Context.AUDIO_SERVICE)
        audio_manager.requestAudioFocus(None, AudioManager.STREAM_ALARM, AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
        
        app_dir = service.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"
        
        if os.path.exists(app_dir):
            player = MediaPlayer()
            player.setWakeMode(service, PowerManager.PARTIAL_WAKE_LOCK)
            
            attr_builder = autoclass('android.media.AudioAttributes$Builder')()
            attr_builder.setUsage(AudioAttributes.USAGE_ALARM)
            attr_builder.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            
            player.setAudioAttributes(attr_builder.build())
            player.setDataSource(app_dir)
            player.prepare()
            player.start()
    except Exception as e:
        print(f"Erro ao tocar no Service: {e}")

# 1. Ativa a notificação fixa (Srvsom)
iniciar_foreground_notification()

# 2. Segura a CPU
lock = adquirir_wake_lock()

# 3. Loop do alarme (Vibração + Som) a cada 5 segundos
while True:
    vibrar_dispositivo(500)  # Vibra por meio segundo
    tocar_som()             # Toca a sirene
    time.sleep(5)