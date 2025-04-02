FROM alpine:latest
RUN apk --update --no-cache add docker && \
  echo "*/1 * * * * docker exec firebase /usr/local/bin/export-firebase.sh> /dev/null 2>&1" >> /etc/crontabs/root
