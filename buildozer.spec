[app]

title = a_teste_som
package.name = atestesom
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,locale,mp3
version = 0.1
requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 0

# Permissões necessárias para WakeLock, Notificações e Foreground Service
#android.permissions = WAKE_LOCK, VIBRATE, FOREGROUND_SERVICE, FOREGROUND_SERVICE_MEDIA_PLAYBACK, POST_NOTIFICATIONS
#android.permissions = FOREGROUND_SERVICE, FOREGROUND_SERVICE_MEDIA_PLAYBACK, POST_NOTIFICATIONS, WAKE_LOCK, VIBRATE, SYSTEM_ALERT_WINDOW, USE_FULL_SCREEN_INTENT
android.permissions = FOREGROUND_SERVICE, FOREGROUND_SERVICE_MEDIA_PLAYBACK, POST_NOTIFICATIONS, WAKE_LOCK, VIBRATE, SYSTEM_ALERT_WINDOW, USE_FULL_SCREEN_INTENT, SCHEDULE_EXACT_ALARM

android.service_foreground_types = mediaPlayback

# Declaração do serviço em segundo plano
#services = srvsom:service.py:foreground

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1