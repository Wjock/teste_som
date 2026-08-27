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
        
        CHANNEL_ID = "canal_srvsom_prioridade_maxima"
        
        # Canal IMPORTANCE_HIGH obriga o Android a mostrar o ícone na barra de status
        channel = NotificationChannel(
            CHANNEL_ID,
            "Servico Srvsom Ativo",
            NotificationManager.IMPORTANCE_HIGH
        )
        channel.setLockscreenVisibility(1)  # VISIBILITY_PUBLIC (Mostra no bloqueio)
        nm.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("Serviço Srvsom em execução permanente")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        builder.setOngoing(True)  # Torna a notificação fixa (não pode ser apagada com deslize)
        
        # Dispara o serviço em primeiro plano real
        service.startForeground(101, builder.build())
        print("startForeground executado com sucesso com prioridade MAXIMA!")
    except Exception as e:
        print(f"Erro ao ativar Foreground real: {e}")

def executar_pulso():
    PythonService = autoclass('org.kivy.android.PythonService')
    Context = autoclass('android.content.Context')
    service = PythonService.mContext

    # 1. Vibração de hardware
    try:
        vibrator = service.getSystemService(Context.VIBRATOR_SERVICE)
        if vibrator and vibrator.hasVibrator():
            vibrator.vibrate(500)
    except Exception as e_vib:
        print(f"Erro vibra: {e_vib}")

    # 2. Som via MediaPlayer
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
        print(f"Erro som: {e_som}")

# Ativa o primeiro plano obrigatoriamente
iniciar_foreground()

# Loop contínuo a cada 5 segundos
while True:
    try:
        executar_pulso()
    except Exception as e_loop:
        print(f"Erro no loop: {e_loop}")
        
    time.sleep(5)