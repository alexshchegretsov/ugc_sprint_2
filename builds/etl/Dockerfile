FROM python:3.8
WORKDIR app/
COPY requirements.txt /app
RUN python -m pip install --upgrade pip && \
 python -m pip install -r requirements.txt && \
 mkdir -p /var/log/supervisor && \
 mkdir -p /etc/supervisor/conf.d && \
 mkdir -p /var/log/etl
COPY ./etl /app
COPY ./conf/supervisord.conf /etc/supervisor
CMD /usr/local/bin/supervisord