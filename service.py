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
        
        CHANNEL_ID = "canal_alarme_a31_v2"
        
        notification_manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
        channel = NotificationChannel(
            CHANNEL_ID,
            "Servico Alarme Ativo",
            NotificationManager.IMPORTANCE_HIGH
        )
        notification_manager.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Alarme em segundo plano ativo")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        
        notification = builder.build()
        service.startForeground(101, notification)
    except Exception as e:
        print(f"Erro no Foreground: {e}")

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
        print(f"Erro no WakeLock: {e}")
        return None

def disparar_alarme_e_vibracao():
    """Dispara som e vibração usando as APIs nativas de Alarme do Android."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        RingtoneManager = autoclass('android.media.RingtoneManager')
        Uri = autoclass('android.net.Uri')
        
        service = PythonService.mContext

        # 1. Toca o Som via RingtoneManager (Usando o som de ALARME padrão do Android ou o arquivo)
        try:
            app_dir = service.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"
            if os.path.exists(app_dir):
                file_obj = autoclass('java.io.File')(app_dir)
                sound_uri = Uri.fromFile(file_obj)
            else:
                sound_uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)

            ringtone = RingtoneManager.getRingtone(service, sound_uri)
            
            # Configura como Canal de Alarme
            AudioAttributes = autoclass('android.media.AudioAttributes')
            attr_builder = autoclass('android.media.AudioAttributes$Builder')()
            attr_builder.setUsage(AudioAttributes.USAGE_ALARM)
            attr_builder.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            ringtone.setAudioAttributes(attr_builder.build())
            
            ringtone.play()
        except Exception as e_sound:
            print(f"Erro no som: {e_sound}")

        # 2. Aciona a Vibração
        try:
            vibrator = service.getSystemService(Context.VIBRATOR_SERVICE)
            if vibrator and vibrator.hasVibrator():
                vibrator.vibrate(500)  # 500 ms
        except Exception as e_vib:
            print(f"Erro na vibracao: {e_vib}")

    except Exception as e:
        print(f"Erro geral no disparo: {e}")

# 1. Ativa a notificação fixa de primeiro plano
iniciar_foreground_notification()

# 2. Ativa o WakeLock do processador
lock = adquirir_wake_lock()

# 3. Loop contínuo a cada 5 segundos
while True:
    disparar_alarme_e_vibracao()
    time.sleep(5)