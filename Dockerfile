# example: Python 3.11 on Debian slim
FROM python:3.10-slim

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel gunicorn

# KROK 1: Zainstaluj Cython i numpy PRZED madmom
RUN pip install --no-cache-dir "Cython>=0.29.33" "numpy>=1.23.0,<1.26"

# KROK 2: Zainstaluj Flask
RUN pip install --no-cache-dir Flask

# KROK 3: Skopiuj requirements i zainstaluj resztę
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir madmom==0.16.1 ffmpeg-python

RUN pip install -r requirements.txt

# Weryfikacja instalacji
#RUN python -c "import flask; import madmom; print('All modules installed successfully')"

ENTRYPOINT ["python", "app.py"]

COPY . /app

EXPOSE 5000
#CMD python ./app.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]