import os
import time
from jnius import autoclass

def adquirir_wake_lock():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        PowerManager = autoclass('android.os.PowerManager')
        
        service = PythonService.mContext
        pm = service.getSystemService(Context.POWER_SERVICE)
        wake_lock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "TesteSom:ServiceLock")
        wake_lock.acquire()
    except Exception as e:
        print(f"Erro WakeLock no Service: {e}")

def tocar_e_vibrar():
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        service = PythonService.mContext

        # 1. Vibrar por 1 segundo
        vibrator = service.getSystemService(Context.VIBRATOR_SERVICE)
        if vibrator and vibrator.hasVibrator():
            vibrator.vibrate(1000)

        # 2. Tocar Áudio via MediaPlayer
        caminho_audio = os.path.abspath("sirene.mp3")
        MediaPlayer = autoclass('android.media.MediaPlayer')
        player = MediaPlayer()
        player.setDataSource(caminho_audio)
        player.prepare()
        player.start()
    except Exception as e:
        print(f"Erro ao tocar/vibrar no Service: {e}")

adquirir_wake_lock()

# Loop contínuo a cada 20 segundos
while True:
    time.sleep(20)
    tocar_e_vibrar()