robocopy "%cd%" "%cd%\stroodle-svc" .gitignore
robocopy "%cd%" "%cd%\stroodle-svc" db_actions.js
robocopy "%cd%" "%cd%\stroodle-svc" package.json
robocopy "%cd%" "%cd%\stroodle-svc" package-lock.json
robocopy "%cd%" "%cd%\stroodle-svc" server.js
robocopy "%cd%\data" "%cd%\stroodle-svc\data"
robocopy "%cd%\node_modules" "%cd%\stroodle-svc\node_modules"

cd stroodle-svc

git add .
git commit -m "Cool stuff"
git push heroku master

pause