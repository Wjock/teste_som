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
        
        CHANNEL_ID = "canal_alarme_a31_v5"
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme de Emergencia",
            NotificationManager.IMPORTANCE_HIGH
        )
        nm.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Alarme ativo em segundo plano")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        service.startForeground(101, builder.build())
    except Exception as e:
        print(f"Erro no Foreground: {e}")

def tocar_com_tela_ativa():
    """Acorda o display por 2 segundos para liberar o chip de áudio da Samsung."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        
        service = PythonService.mContext
        pm = service.getSystemService(Context.POWER_SERVICE)
        
        # Flags: SCREEN_BRIGHT_WAKE_LOCK (26) | ACQUIRE_CAUSES_WAKEUP (1) | ON_AFTER_RELEASE (10)
        flags = 26 | 1 | 10
        wake_screen = pm.newWakeLock(flags, "a_teste_som:AcordarTela")
        wake_screen.acquire(2000)  # Segura por 2 segundos para ligar o display
        
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
            
    except Exception as e:
        print(f"Erro ao tocar acendendo a tela: {e}")

# Inicia o serviço
iniciar_foreground()

# Loop contínuo a cada 5 segundos
while True:
    tocar_com_tela_ativa()
    time.sleep(5)