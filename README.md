# 1ra vez

python3 -m venv venv # crea el entorno virtual
source venv/bin/activate # activa el entorno virtual

pip install Flask

pip install -r requirements.txt

pip install -r requirements.txt --upgrade # instalas los paquetes

pip freeze # que esta instalado

deactivate # desactiva el entorno virtual

# 

source venv/bin/activate # activa el entorno virtual
pip install -r requirements.txt --upgrade # instalas los paquetes

#

flask --app main run

flask --app main run --reload


mkdir myproject
cd myproject
py -3 -m venv .venv

flask --app main db init

flask --app main db upgrade

flask --app main stamp head
