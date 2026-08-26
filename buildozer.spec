[app]

# Titulo que aparece abaixo do icone no celular
title = a_teste_som

# Nome interno do pacote (sem underlines ou espacos)
package.name = atestesom
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ogg,wav,mp3

version = 0.1
requirements = hostpython3==3.11.9,python3==3.11.9,kivy==2.3.0

orientation = portrait
fullscreen = 0

# Permissões necessárias para serviços e notificações no Android 13+
android.permissions = INTERNET, WAKE_LOCK, VIBRATE, FOREGROUND_SERVICE, POST_NOTIFICATIONS

# Declaracao do servico em segundo plano
services = srvsom:service.py:foreground

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1