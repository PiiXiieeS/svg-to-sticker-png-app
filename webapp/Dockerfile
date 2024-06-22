FROM python:3.9.16-slim-bullseye

WORKDIR /app

COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

COPY . ./

EXPOSE 3000

# CMD ["python3", "./server.py"]
CMD ["python3", "./src/__init__.py"]