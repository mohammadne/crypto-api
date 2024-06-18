FROM alpine:3.19.1

WORKDIR /sms-monkey

RUN apk update
RUN apk add --no-cache python3 py3-pip
RUN rm /usr/lib/python*/EXTERNALLY-MANAGED && pip3 install flask

COPY ./build/requirements.txt ./
RUN pip3 --no-cache-dir install -r requirements.txt
RUN ls -lah

COPY ./src/ ./

CMD ["python3", "main.py"]
