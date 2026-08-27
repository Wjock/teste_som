import os
import time
from jnius import autoclass

def iniciar_servico_com_alarme():
    """Utiliza o canal de notificação nativo com som e vibração de alta prioridade."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        Uri = autoclass('android.net.Uri')
        File = autoclass('java.io.File')
        
        service = PythonService.mContext
        notification_manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
        
        CHANNEL_ID = "canal_alarme_urgente_v3"
        
        # 1. Configura a saída do som como ALARME no canal do Android
        attr_builder = autoclass('android.media.AudioAttributes$Builder')()
        attr_builder.setUsage(AudioAttributes.USAGE_ALARM)
        attr_builder.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
        audio_attr = attr_builder.build()
        
        # 2. Configura o arquivo de som sirene.mp3 para a notificação
        app_dir = service.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"
        if os.path.exists(app_dir):
            sound_uri = Uri.fromFile(File(app_dir))
        else:
            RingtoneManager = autoclass('android.media.RingtoneManager')
            sound_uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)

        # 3. Cria o canal com IMPORTANCE_HIGH, Som e Padrão de Vibração
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme Sonoro Urgente",
            NotificationManager.IMPORTANCE_HIGH
        )
        channel.setSound(sound_uri, audio_attr)
        channel.enableVibration(True)
        
        # Define o padrão de vibração (espera 0ms, vibra 500ms)
        vibration_pattern = [0, 500]
        channel.setVibrationPattern(vibration_pattern)
        
        notification_manager.createNotificationChannel(channel)
        
        # 4. Monta a notificação do serviço de primeiro plano
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Alarme ativo em segundo plano")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        builder.setOngoing(True)
        
        notification = builder.build()
        service.startForeground(101, notification)
        return notification_manager, builder, CHANNEL_ID
    except Exception as e:
        print(f"Erro ao iniciar o serviço de notificação: {e}")
        return None, None, None

def emitir_pulso_alarme(notification_manager, builder, channel_id):
    """Reenvia a notificação para forçar o disparo do som e da vibração."""
    try:
        if notification_manager and builder:
            # Recompoe a notificação para acionar o canal sonoro/vibratório a cada ciclo
            notification = builder.build()
            notification_manager.notify(101, notification)
    except Exception as e:
        print(f"Erro ao emitir pulso: {e}")

# 1. Inicializa o serviço com canal de alarme e vibração nativos
nm, builder, ch_id = iniciar_servico_com_alarme()

# 2. Segura a CPU em suspensão
try:
    PythonService = autoclass('org.kivy.android.PythonService')
    Context = autoclass('android.content.Context')
    PowerManager = autoclass('android.os.PowerManager')
    service = PythonService.mContext
    pm = service.getSystemService(Context.POWER_SERVICE)
    wake_lock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "a_teste_som:ServiceLock")
    wake_lock.acquire()
except Exception as e:
    print(f"Erro no WakeLock: {e}")

# 3. Loop contínuo a cada 5 segundos
while True:
    emitir_pulso_alarme(nm, builder, ch_id)
    time.sleep(5)