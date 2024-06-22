FROM python:3.9.16-slim-bullseye

WORKDIR /app

COPY requirements.txt ./
RUN pip3 --no-cache-dir install -r requirements.txt

# (Ubuntu) Install libraries needed for CairoSVG
# RUN apt-get update && apt-get install -y libcairo2-dev=1.16.0-4ubuntu1 libffi-dev-3.4.6

# (M1 Mac, arch x86) Install libraries needed for CairoSVG
RUN apt-get update && apt-get install -y libcairo2-dev libffi-dev

COPY . ./