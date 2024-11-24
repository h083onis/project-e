FROM python:3.10

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir Flask 

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]