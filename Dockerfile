FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential \
    python3-setuptools \
    python3-dev \
    python3-pip \
    libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy local into docker
COPY . /app

# Install dependencies
WORKDIR /app
RUN pip3 install pip --upgrade && pip install -r requirements.txt
CMD [ "python3", "main.py" ]
