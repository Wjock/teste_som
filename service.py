import os
import time
from jnius import autoclass

def iniciar_foreground_notification():
    """Exibe o ícone fixo na barra para o Android não congelar o app ao apagar a tela."""
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
        builder.setContentText("Serviço em segundo plano em execução")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        notification = builder.build()
        
        # Coloca o serviço em Foreground (Notificação ativa)
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

def tocar_som():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mContext
        
        app_dir = service.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"
        
        if os.path.exists(app_dir):
            MediaPlayer = autoclass('android.media.MediaPlayer')
            player = MediaPlayer()
            player.setDataSource(app_dir)
            player.prepare()
            player.start()
    except Exception as e:
        print(f"Erro ao tocar no Service: {e}")

# 1. Ativa a notificação visível na barra do Android
iniciar_foreground_notification()

# 2. Segura a CPU
lock = adquirir_wake_lock()

# 3. Loop do alarme a cada 5 segundos
while True:
    tocar_som()
    time.sleep(5)