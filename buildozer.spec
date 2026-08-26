[app]

# (str) Title of your application
title = Teste Som

# (str) Package name
package.name = testesom

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (include the optionals)
source.include_exts = py,png,jpg,kv,atlas,ogg,wav,mp3

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = hostpython3==3.11.9,python3==3.11.9,kivy==2.3.0

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# WAKE_LOCK ajuda o app a solicitar ao Android para nao dormir imediatamente
android.permissions = INTERNET, WAKE_LOCK

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (list) List of architectures to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1
