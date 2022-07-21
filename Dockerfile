FROM node:16.13-bullseye

RUN apt-get update && apt-get upgrade -y

# install ganache-cli
RUN npm install ganache-cli@6.12.2 --global

# install python3 and pip
RUN apt-get install -y python3 python3-dev python3-pip

# install brownie
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /possums

# install compiler before importing sources
COPY install_compiler.py install_compiler.py
RUN python3 install_compiler.py

# install npm dependencies
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install

COPY brownie-config.yaml brownie-config.yaml
COPY scripts scripts
COPY contracts contracts
COPY tests tests

RUN brownie compile

ENTRYPOINT ["brownie"]
CMD ["console"]
