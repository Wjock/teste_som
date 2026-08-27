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
        
        CHANNEL_ID = "canal_alarme_activity"
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

def disparar_intent_para_activity():
    """Acorda a Activity principal para forçar o acendimento da tela e liberação do áudio."""
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Intent = autoclass('android.content.Intent')
        
        service = PythonService.mContext
        
        # Cria a Intent para a Activity principal (PythonActivity)
        intent = Intent(service, autoclass('org.kivy.android.PythonActivity'))
        # FLAG_ACTIVITY_NEW_TASK (268435456) | FLAG_ACTIVITY_SINGLE_TOP (536870912) | FLAG_ACTIVITY_REORDER_TO_FRONT (131072)
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
        
        # Dispara a Activity que está registrada com as flags de acender a tela
        service.startActivity(intent)
    except Exception as e:
        print(f"Erro ao disparar Intent para Activity: {e}")

# 1. Registra o serviço de primeiro plano
iniciar_foreground()

# 2. Mantém o WakeLock básico da CPU
try:
    PythonService = autoclass('org.kivy.android.PythonService')
    Context = autoclass('android.content.Context')
    PowerManager = autoclass('android.os.PowerManager')
    service = PythonService.mContext
    pm = service.getSystemService(Context.POWER_SERVICE)
    wake_lock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "a_teste_som:LoopLock")
    wake_lock.acquire()
except Exception as e:
    print(f"Erro WakeLock: {e}")

# 3. Loop contínuo: acorda a Activity a cada 5 segundos
while True:
    disparar_intent_para_activity()
    time.sleep(5)