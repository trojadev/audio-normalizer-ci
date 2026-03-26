ARG PYTHON_VER=3.12
FROM python:${PYTHON_VER}-slim

RUN apt-get update && apt-get -y install sox 

WORKDIR /app

RUN groupadd -g 1000 "appgroup" && \
    useradd -u 1000 "appuser" -g 1000 -s /bin/bash

RUN mkdir -p /data/processed_files/ && chown -R 1000:1000 /data/processed_files/

USER appuser

COPY --chown=appuser:appgroup audio-processor.py /app


ENTRYPOINT ["/usr/local/bin/python", "audio-processor.py" ]
