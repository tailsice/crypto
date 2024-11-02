 docker build --platform linux/amd64 -t crypto-observe .
 docker stop crypto-observe
 docker rm crypto-observe
 docker run -itd -v ./app.dev.ini:/app/app.ini --name crypto-observe crypto-observe