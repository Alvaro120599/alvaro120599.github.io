flask --app main db init
flask --app main db migrate
flask --app main db upgrade

flask --app main shell