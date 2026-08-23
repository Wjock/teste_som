[app]

title = Teste Som
package.name = testesom
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ogg,wav,mp3

version = 0.1
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 34
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1