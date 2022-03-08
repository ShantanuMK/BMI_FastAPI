FROM python:3.8
ENV DEPLOYMENT_MODE=DEV
COPY app/ /app


RUN pip install -r requirements.txt

WORKDIR /app
EXPOSE 8080

CMD ["python", "main.py"]
