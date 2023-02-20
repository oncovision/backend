FROM python:3.8.15

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# Bundle app source
COPY . .

CMD [ "python", "main.py" ]

