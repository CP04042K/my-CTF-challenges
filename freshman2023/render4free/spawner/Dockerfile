FROM node:20-alpine

RUN apk add --no-cache docker-cli

COPY ./deploy /deploy
RUN mkdir /www
COPY ./www/package.json ./www/yarn.lock /www/
WORKDIR /www

RUN yarn
COPY ./www /www

RUN chmod +x /www/run.sh
ENTRYPOINT ["/www/run.sh"]
