import os
import time
from jnius import autoclass

def criar_notificacao_foreground():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        
        service = PythonService.mContext
        nm = service.getSystemService(Context.NOTIFICATION_SERVICE)
        
        CHANNEL_ID = "canal_srvsom_v9"
        
        # Cria canal com prioridade maxima (IMPORTANCE_HIGH = 4)
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme Srvsom",
            4
        )
        nm.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Serviço Srvsom Rodando")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        builder.setOngoing(True)
        
        service.startForeground(101, builder.build())
    except Exception as e:
        print(f"Erro notificacao: {e}")

def disparar_som_e_vibracao():
    """Dispara os eventos isoladamente."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        service = PythonService.mContext
        
        # 1. Acorda Tela (PowerManager)
        try:
            PowerManager = autoclass('android.os.PowerManager')
            pm = service.getSystemService(Context.POWER_SERVICE)
            # SCREEN_BRIGHT_WAKE_LOCK (26) | ACQUIRE_CAUSES_WAKEUP (1) | ON_AFTER_RELEASE (10)
            wake_lock = pm.newWakeLock(26 | 1 | 10, "a_teste_som:Acorda")
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

        # 3. Som Sirene.mp3
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
        print(f"Erro Geral Disparo: {e}")

# 1. Inicia notificação no topo
criar_notificacao_foreground()

# 2. Loop de 5 segundos
while True:
    disparar_som_e_vibracao()
    time.sleep(5)