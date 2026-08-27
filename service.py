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
        
        CHANNEL_ID = "canal_alarme_a31_v6"
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme de Emergencia",
            NotificationManager.IMPORTANCE_HIGH
        )
        nm.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Serviço Srvsom em execução")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        service.startForeground(101, builder.build())
    except Exception as e:
        print(f"Erro no Foreground: {e}")

def agendar_e_tocar_alarme():
    """Utiliza o AlarmManager para furar o Doze Mode da Samsung e acender a CPU/Áudio."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        
        service = PythonService.mContext
        
        # 1. Força o acendimento da tela e atração da CPU
        pm = service.getSystemService(Context.POWER_SERVICE)
        # SCREEN_BRIGHT_WAKE_LOCK (26) | FULL_WAKE_LOCK (10) | ACQUIRE_CAUSES_WAKEUP (268435456 = 0x10000000)
        flags = 0x10000000 | 26 | 10
        wake = pm.newWakeLock(flags, "a_teste_som:AlarmWake")
        wake.acquire(3000)  # Força o acendimento por 3 segundos
        
        # 2. Executa o MediaPlayer configurado como ALARME de alta prioridade
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
        print(f"Erro ao disparar alarme em suspensão: {e}")

# 1. Inicia o serviço de primeiro plano
iniciar_foreground()

# 2. Loop com garantia de liberação de memória e Waking
while True:
    agendar_e_tocar_alarme()
    time.sleep(5)