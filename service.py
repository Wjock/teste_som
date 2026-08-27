import os
import time
from jnius import autoclass

def iniciar_foreground_notification():
    """Mantém a notificação ativa no painel do Android."""
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

def tocar_som_com_wakelock():
    """Configura o som como ALARME para disparar na tela bloqueada."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        
        service = PythonService.mContext
        app_dir = service.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"
        
        if os.path.exists(app_dir):
            player = MediaPlayer()
            
            # 1. Dá permissão de hardware para o tocador acionar o processador
            player.setWakeMode(service, PowerManager.PARTIAL_WAKE_LOCK)
            
            # 2. Define o canal de áudio como ALARME (impede o silenciamento na suspensão)
            attr_builder = autoclass('android.media.AudioAttributes$Builder')()
            attr_builder.setUsage(AudioAttributes.USAGE_ALARM)
            attr_builder.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            
            player.setAudioAttributes(attr_builder.build())
            player.setDataSource(app_dir)
            player.prepare()
            player.start()
    except Exception as e:
        print(f"Erro ao tocar no Service: {e}")

# Inicia a notificação e o loop
iniciar_foreground_notification()

while True:
    tocar_som_com_wakelock()
    time.sleep(5)