FROM python:3.12.2

EXPOSE 8000
WORKDIR /app

COPY requirements.txt . 
RUN pip install -r requirements.txt 

# enabled hot reload with volume on compose.yaml
# COPY . .

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
