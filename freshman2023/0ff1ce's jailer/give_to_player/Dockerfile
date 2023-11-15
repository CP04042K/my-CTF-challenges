FROM python:3.10-bullseye

RUN useradd -ms /bin/bash ctf_user
RUN groupadd ctf && \
    usermod -a -G ctf ctf_user

RUN mkdir /app
COPY --chown=ctf_user:ctf main.py /app
COPY flag.txt /
RUN pip install jinja2
RUN apt-get -y update 
RUN apt-get -y install xinetd

COPY pyjail.xinetd /etc/xinetd.d/pyjail
COPY init.sh /app/init.sh
RUN chmod +x /app/init.sh
RUN chmod +x /app/main.py

USER ctf_user
RUN service xinetd restart
ENTRYPOINT [ "/app/init.sh" ]