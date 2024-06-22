# SVGtoStickerPNG App

![Python README Badge](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![Docker README Badge](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white) ![Flask README Badge](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![Redis README Badge](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)

Webapp for converting SVG logos to sticker PNG files. Processing images with the Python OpenCV library. Built with Flask (server-side rendering + backend), Redis (Messaging Queue), and Minio (object storage).

![Flask App Architecture Diagram](./.github/diagram.png)

![Frontend Screenshot](./.github/frontend-screenshot.png)

## Prerequisites

- Docker installed ([documentation](https://docs.docker.com/get-docker/))

## Run Locally

```sh
git clone https://github.com/spencerlepine/svg-to-sticker-png-app.git
cd svg-to-sticker-png-app
docker-compose up
# view: http://localhost:3000
```

## Tech Stack

- Python: v3.9
- Flask: light-weight web-app framework (python) ([documentation](https://github.com/pallets/flask))
- Redis: in-memory message queue ([documentation](https://github.com/redis/redis-py))
- Minio: block storage ([documentation](https://min.io/docs/minio/linux/developers/python/API.html))
- OpenCV: python image manipulation library ([documentation](https://github.com/opencv/opencv-python)) (+ [CarioSVG](https://cairosvg.org/documentation/))
s