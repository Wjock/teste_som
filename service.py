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
        
        CHANNEL_ID = "canal_alarm_manager_v1"
        channel = NotificationChannel(
            CHANNEL_ID,
            "Alarme de Emergência Nativo",
            NotificationManager.IMPORTANCE_HIGH
        )
        nm.createNotificationChannel(channel)
        
        builder = NotificationBuilder(service, CHANNEL_ID)
        builder.setContentTitle("a_teste_som")
        builder.setContentText("AlarmManager Ativo em Segundo Plano")
        builder.setSmallIcon(service.getApplicationInfo().icon)
        builder.setOngoing(True)
        
        service.startForeground(101, builder.build())
    except Exception as e:
        print(f"Erro no Foreground: {e}")

def disparar_som_e_vibracao_nativo():
    """Acorda o hardware via acendimento de tela, toca e vibra."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        service = PythonService.mContext

        # 1. Acorda o Display
        try:
            PowerManager = autoclass('android.os.PowerManager')
            pm = service.getSystemService(Context.POWER_SERVICE)
            # 26 = SCREEN_BRIGHT_WAKE_LOCK | 1 = ACQUIRE_CAUSES_WAKEUP | 10 = ON_AFTER_RELEASE
            wake_lock = pm.newWakeLock(26 | 1 | 10, "a_teste_som:AlarmManagerWake")
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

        # 3. Som Sirene
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
        print(f"Erro no disparo de hardware: {e}")

def agendar_proxima_execucao():
    """Utiliza a API AlarmManager para instruir o Kernel do Android a disparar em 5 segundos."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        Intent = autoclass('android.content.Intent')
        PendingIntent = autoclass('android.app.PendingIntent')
        System = autoclass('java.lang.System')
        
        service = PythonService.mContext
        alarm_manager = service.getSystemService(Context.ALARM_SERVICE)
        
        # Intent apontando para o próprio serviço
        intent = Intent(service, service.getClass())
        # FLAG_UPDATE_CURRENT (134217728) | FLAG_IMMUTABLE (67108864)
        pending_intent = PendingIntent.getService(service, 0, intent, 134217728 | 67108864)
        
        # Tempo atual + 5000ms (5 segundos)
        trigger_at_millis = System.currentTimeMillis() + 5000
        
        # setExactAndAllowWhileIdle = Garante o disparo MESMO em suspensão profunda (Doze Mode)
        # RTC_WAKEUP = 0 (Acorda a CPU se estiver dormindo)
        alarm_manager.setExactAndAllowWhileIdle(0, trigger_at_millis, pending_intent)
        print("Próximo alarme agendado no AlarmManager nativo com sucesso!")
    except Exception as e:
        print(f"Erro ao agendar AlarmManager: {e}")

# 1. Inicia o serviço de primeiro plano
iniciar_foreground()

# 2. Executa o pulso atual de som e vibração
disparar_som_e_vibracao_nativo()

# 3. Agenda a próxima execução no Kernel e encerra o ciclo da CPU
agendar_proxima_execucao()