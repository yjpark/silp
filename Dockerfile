FROM python:alpine3.17

COPY . /silp

RUN cd /silp && python /silp/setup.py install

WORKDIR /data

ENTRYPOINT ["silp"]
