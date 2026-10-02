FROM python:3.9

WORKDIR /app

COPY requirements.txt /app
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*


# Install app dependencies
RUN pip install --no-cache-dir "mysqlclient<2.2.8"
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
