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
        AudioAttributes = autoclass('android.media.AudioAttributes')
        Uri = autoclass('android.net.Uri')
        File = autoclass('java.io.File')
        
        service = PythonService.mContext
        nm = service.getSystemService(Context.NOTIFICATION_SERVICE)
        
        CHANNEL_ID = "canal_srvsom_alerta_v8"
        
        # 1. Configura atributos de Alarme diretamente para a notificação
        attr_builder = autoclass('android.media.AudioAttributes$Builder')()
        attr_builder.setUsage(AudioAttributes.USAGE_ALARM)
        attr_builder.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
        audio_attr = attr_builder.build()
        
        # 2. Localiza o áudio sirene.mp3
        app_dir = service.getFilesDir().getAbsolutePath() + "/app/sirene.mp3"
        if os.path.exists(app_dir):
            sound_uri = Uri.fromFile(File(app_dir))
        else:
            RingtoneManager = autoclass('android.media.RingtoneManager')
            sound_uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)

        # 3. Cria o Canal com prioridade de ALERTA (IMPORTANCE_HIGH), Som e Vibração
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme Ativo Srvsom",
            NotificationManager.IMPORTANCE_HIGH  # Garante que NÂO fique Silencioso
        )
        channel.setSound(sound_uri, audio_attr)
        channel.enableVibration(True)
        channel.setVibrationPattern([0, 500])
        channel.setLockscreenVisibility(1)  # Mostra na tela de bloqueio
        
        nm.createNotificationChannel(channel)
        
        # 4. Monta a notificação permanente de primeiro plano
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Alarme em segundo plano rodando")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        builder.setOngoing(True)
        
        service.startForeground(101, builder.build())
        print("Serviço iniciado em Primeiro Plano com Sucesso!")
    except Exception as e:
        print(f"Erro ao iniciar Foreground: {e}")

def executar_pulso_alarme():
    """Acorda a CPU/Tela e dispara o som e a vibração em suspensão."""
    PythonService = autoclass('org.kivy.android.PythonService')
    Context = autoclass('android.content.Context')
    service = PythonService.mContext

    # 1. Acorda a tela por 1.5s
    try:
        PowerManager = autoclass('android.os.PowerManager')
        pm = service.getSystemService(Context.POWER_SERVICE)
        # 26 = SCREEN_BRIGHT_WAKE_LOCK | 1 = ACQUIRE_CAUSES_WAKEUP | 10 = ON_AFTER_RELEASE
        wake_lock = pm.newWakeLock(26 | 1 | 10, "a_teste_som:AcordaLock")
        wake_lock.acquire(1500)
    except Exception as e_wake:
        print(f"Erro no WakeLock: {e_wake}")

    # 2. Vibração de hardware
    try:
        vibrator = service.getSystemService(Context.VIBRATOR_SERVICE)
        if vibrator and vibrator.hasVibrator():
            vibrator.vibrate(500)
    except Exception as e_vib:
        print(f"Erro na vibracao: {e_vib}")

    # 3. Toca o Som Sirene.mp3
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
    except Exception as e_som:
        print(f"Erro no som: {e_som}")

# Inicia o serviço com o novo canal de ALERTA MÁXIMO
iniciar_foreground()

# Loop contínuo a cada 5 segundos
while True:
    try:
        executar_pulso_alarme()
    except Exception as e_loop:
        print(f"Erro no loop: {e_loop}")
        
    time.sleep(5)