FROM python:3.8
ENV DEPLOYMENT_MODE=DEV
COPY . /app

WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]
