FROM python:3.10

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "model.py"]