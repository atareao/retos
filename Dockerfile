FROM alpine:3.15

ENV TZ=Europe/Madrid
LABEL maintainer="Lorenzo Carbonell <a.k.a. atareao> lorenzo.carbonell.cerezo@gmail.com"

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

RUN echo "**** install Python ****" && \
    apk add --update --no-cache \
            tini==0.19.0-r0 \
            tzdata==2021e-r0 \
            python3==3.9.7-r4 && \
    rm -rf /var/lib/apt/lists/* && \
    echo "**** create user ****" && \
    addgroup dockerus && \
    adduser -h /app -G dockerus -D dockerus && \
    mkdir -p ${VIRTUAL_ENV} && \
    chown -R dockerus:dockerus ${VIRTUAL_ENV} && \
    mkdir -p /app/database && \
    chown -R dockerus:dockerus /app

COPY entrypoint.sh requirements.txt /
USER dockerus
RUN echo "**** install Python dependencies **** " && \
    python3 -m venv ${VIRTUAL_ENV} && \
    ${VIRTUAL_ENV}/bin/pip install --upgrade pip && \
    ${VIRTUAL_ENV}/bin/pip install --no-cache-dir -r /requirements.txt

WORKDIR /app

COPY --chown=dockerus:dockerus ./app /app/

ENTRYPOINT ["tini", "--"]
CMD ["/bin/sh", "/entrypoint.sh"]
