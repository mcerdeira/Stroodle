call npm run build

robocopy "%cd%\dist" "%cd%\stroodle-app" /e /move

cd stroodle-app

git add .
git commit -m "Cool stuff"
git push heroku master

pause