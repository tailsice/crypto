 docker build --platform linux/amd64 -t crypto-observe .
 docker stop crypto-observe
 docker rm crypto-observe

 # 把 local的app.dev.ini 放到container 的/app/app.ini
 # 請自行根據實際狀況調整
 docker run -itd -v ./app.dev.ini:/app/app.ini --name crypto-observe crypto-observe