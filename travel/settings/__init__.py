
#* Эта конструкция будет работать на внешних серверах, например, Heroku
from .production import * 
# при запуске данного проекта, все настройки из файла production.py будут импортированы в __iit__.py и запущены

try:
    from .local_settings import *
except ImportError:
    pass
# если есть файл local_settings => 
# => те настройки, который есть в этом файле local_settings будут затянуты позже, 
# т.е. они перезапишут все те настройки, которые будут указаны в файле production.py =>
# => на локальном сервере у нас будет файл local_settings.py, а на внешнем сервере (Heroku) его не будет, 
# а будет production.py