import os
import time
from jnius import autoclass

def rodar_servico():
    # Carrega as classes Android dentro do escopo da função para evitar crash na subida
    PythonService = autoclass('org.kivy.android.PythonService')
    Context = autoclass('android.content.Context')
    PowerManager = autoclass('android.os.PowerManager')
    MediaPlayer = autoclass('android.media.MediaPlayer')
    AudioAttributes = autoclass('android.media.AudioAttributes')
    NotificationBuilder = autoclass('android.app.Notification$Builder')
    NotificationManager = autoclass('android.app.NotificationManager')
    NotificationChannel = autoclass('android.app.NotificationChannel')

    service = PythonService.mContext

    # 1. Configura e exibe a Notificação de Foreground
    try:
        CHANNEL_ID = "canal_alarme_a31"
        notification_manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
        
        # IMPORTANCE_LOW (2) para notificação limpa ou HIGH para prioridade
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme em Segundo Plano",
            NotificationManager.IMPORTANCE_HIGH
        )
        notification_manager.createNotificationChannel(channel)

        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Serviço de alarme ativo")
        builder.setSmallIcon(service.getApplicationInfo().icon)

        # 101 é o ID da notificação. 2 = FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK no Android
        try:
            service.startForeground(101, builder.build(), 2)
        except Exception:
            service.startForeground(101, builder.build())
    except Exception as e:
        print(f"Erro ao iniciar Notificacao: {e}")

    # 2. Adquire o WakeLock para impedir a CPU do Galaxy A31 de dormir
    pm = service.getSystemService(Context.POWER_SERVICE)
    wake_lock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "a_teste_som:CpuLock")
    wake_lock.acquire()

    # 3. Caminho do arquivo
    app_dir = service.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"

    # 4. Loop contínuo de áudio
    while True:
        if os.path.exists(app_dir):
            try:
                player = MediaPlayer()
                player.setWakeMode(service, PowerManager.PARTIAL_WAKE_LOCK)
                
                # Configura como ALARME
                attr_builder = autoclass('android.media.AudioAttributes$Builder')()
                attr_builder.setUsage(AudioAttributes.USAGE_ALARM)
                attr_builder.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                
                player.setAudioAttributes(attr_builder.build())
                player.setDataSource(app_dir)
                player.prepare()
                player.start()
            except Exception as e:
                print(f"Erro ao tocar audio no loop: {e}")
        
        time.sleep(5)

if __name__ == '__main__':
    rodar_servico()