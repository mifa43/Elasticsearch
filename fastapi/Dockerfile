FROM udomiljubimca/base-image:1.0

ADD ./requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt && \
    chown -R appuser:root /app && \
    chmod -R g=u /app

ADD ./server.sh ./src /app/

WORKDIR /app

USER appuser

EXPOSE 8080

CMD ["/bin/bash", "server.sh"]