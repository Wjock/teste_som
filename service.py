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
        
        CHANNEL_ID = "canal_srvsom_v7"
        channel = NotificationChannel(
            CHANNEL_ID,
            "Servico Srvsom Ativo",
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

def executar_pulso_alarme():
    """Executa o disparo isolando cada componente do hardware para evitar crash do serviço."""
    PythonService = autoclass('org.kivy.android.PythonService')
    Context = autoclass('android.content.Context')
    service = PythonService.mContext

    # 1. TENTA ACENDER A TELA (Comando Acorda em bloco protegido)
    try:
        PowerManager = autoclass('android.os.PowerManager')
        pm = service.getSystemService(Context.POWER_SERVICE)
        # 26 = SCREEN_BRIGHT_WAKE_LOCK | 1 = ACQUIRE_CAUSES_WAKEUP
        wake_lock = pm.newWakeLock(27, "a_teste_som:AcordaLock")
        wake_lock.acquire(1500)  # Segura por 1.5s e libera automaticamente pelo sistema
    except Exception as e_wake:
        print(f"Erro no WakeLock de tela: {e_wake}")

    # 2. TENTA VIBRAR (Motor de Vibração)
    try:
        vibrator = service.getSystemService(Context.VIBRATOR_SERVICE)
        if vibrator and vibrator.hasVibrator():
            vibrator.vibrate(500)
    except Exception as e_vib:
        print(f"Erro na vibracao: {e_vib}")

    # 3. TENTA TOCAR O SOM (MediaPlayer com Atributo de Alarme)
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

# 1. Ativa a notificação fixa do Srvsom
iniciar_foreground()

# 2. Loop contínuo a cada 5 segundos blindado contra exceções
while True:
    try:
        executar_pulso_alarme()
    except Exception as e_loop:
        print(f"Erro geral no loop: {e_loop}")
        
    time.sleep(5)