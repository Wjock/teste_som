[app]

title = Teste Som
package.name = testesom
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ogg,wav,mp3

version = 0.1
requirements = hostpython3==3.11.9,python3==3.11.9,kivy==2.3.0

orientation = portrait
fullscreen = 0

# Permissões para manter CPU ativa e disparar o motor de vibração
android.permissions = INTERNET, WAKE_LOCK, VIBRATE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1