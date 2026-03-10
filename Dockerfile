FROM alpine:3.23.3

RUN apk update && apk add --no-cache python3 sox

WORKDIR /app

COPY audio-processor.py /app

ENTRYPOINT ["/usr/bin/python3", "audio-processor.py" ]