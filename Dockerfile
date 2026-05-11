FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /online_shop

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:store_app", "--host", "0.0.0.0", "--port", "8000"]