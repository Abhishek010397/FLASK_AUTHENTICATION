FROM 2307297/rpiflaskbase:latest
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5001
