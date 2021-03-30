FROM python:3.6-slim-buster AS base
# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ARG ssh_prv_key

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc python3-dev build-essential openssh-client curl

RUN mkdir -p /etc/secrets && mkdir -p /srv/service-dwstatus
RUN mkdir -p ~/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan -t rsa github.com > ~/.ssh/known_hosts

RUN curl -sSL -o /tmp/summon.tar.gz https://github.com/cyberark/summon/releases/download/v0.8.1/summon-linux-amd64.tar.gz && \
    tar -C /usr/local/bin -zxvf /tmp/summon.tar.gz >/dev/null && \
    rm /tmp/summon.tar.gz

RUN curl -sSL -o /tmp/summon-aws-secrets.tar.gz https://github.com/cyberark/summon-aws-secrets/releases/download/v0.3.0/summon-aws-secrets-linux-amd64.tar.gz && \
    mkdir -p /usr/local/lib/summon && \
    tar -C /usr/local/lib/summon -zxvf /tmp/summon-aws-secrets.tar.gz && \
    rm /tmp/summon-aws-secrets.tar.gz

RUN pip3 install pipenv

WORKDIR /srv/service-dwstatus
COPY . /srv/service-dwstatus

RUN pipenv install .

EXPOSE 80

RUN chmod +x /srv/service-dwstatus/.docker/entrypoint.sh
ENTRYPOINT ["sh", "/srv/service-dwstatus/.docker/entrypoint.sh"]

CMD [ "start" ]
