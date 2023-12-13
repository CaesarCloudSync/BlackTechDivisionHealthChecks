git add .
git commit -m "$1"
git push origin master:main
docker build -t palondomus/btdhealthcheckstoken:latest .
docker push palondomus/btdhealthcheckstoken:latest
docker run -it -p 8080:8080 palondomus/btdhealthcheckstoken:latest