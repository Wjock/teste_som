import os
import time
from jnius import autoclass

# Classes Android Nativas via PyJnius
PythonService = autoclass('org.kivy.android.PythonService')
Context = autoclass('android.content.Context')
PowerManager = autoclass('android.os.PowerManager')
MediaPlayer = autoclass('android.media.MediaPlayer')
AudioAttributes = autoclass('android.media.AudioAttributes')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationManager = autoclass('android.app.NotificationManager')
NotificationChannel = autoclass('android.app.NotificationChannel')

service = PythonService.mContext

def iniciar_foreground_notification():
    """Garante prioridade máxima para a CPU não dormir em suspensão."""
    try:
        CHANNEL_ID = "canal_alarme_prioritario"
        
        notification_manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
        
        # IMPORTANCE_HIGH (3) impede que a One UI silencie o serviço com tela bloqueada
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme Continuo",
            NotificationManager.IMPORTANCE_HIGH
        )
        notification_manager.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Serviço de alarme em execução")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        notification = builder.build()
        service.startForeground(101, notification)
    except Exception as e:
        print(f"Erro no Foreground: {e}")

def criar_player_global():
    """Instancia o MediaPlayer apenas uma vez com configurações de Alarme e WakeLock."""
    app_dir = service.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"
    
    if not os.path.exists(app_dir):
        print("Arquivo de áudio não encontrado!")
        return None, None

    try:
        player = MediaPlayer()
        # Mantém a CPU ativa enquanto o áudio é reproduzido
        player.setWakeMode(service, PowerManager.PARTIAL_WAKE_LOCK)
        
        # Atributos de Alarme para ignorar modo silencioso de mídia
        attr_builder = autoclass('android.media.AudioAttributes$Builder')()
        attr_builder.setUsage(AudioAttributes.USAGE_ALARM)
        attr_builder.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
        player.setAudioAttributes(attr_builder.build())
        
        player.setDataSource(app_dir)
        player.prepare()
        return player, app_dir
    except Exception as e:
        print(f"Erro ao inicializar MediaPlayer: {e}")
        return None, None

# 1. Eleva a prioridade do serviço
iniciar_foreground_notification()

# 2. Segura o WakeLock global para a CPU não pausar durante o sleep
pm = service.getSystemService(Context.POWER_SERVICE)
wake_lock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "a_teste_som:GlobalLock")
wake_lock.acquire()

# 3. Inicializa o player reutilizável
player, audio_path = criar_player_global()

# 4. Loop de execução contínua
while True:
    if player and audio_path:
        try:
            if player.isPlaying():
                player.stop()
            player.reset()
            player.setDataSource(audio_path)
            player.prepare()
            player.start()
        except Exception as e:
            print(f"Erro no ciclo de reprodução: {e}")
            # Tenta recriar o player caso seja destruído pelo SO
            player, audio_path = criar_player_global()
            
    time.sleep(5)