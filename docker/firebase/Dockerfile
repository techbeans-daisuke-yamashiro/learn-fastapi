FROM google/cloud-sdk:alpine
#FROM python:3.13-alpine
ARG CONTAINER_USER=cloudsdk
ARG WORKSPACE=/opt/firebase
WORKDIR ${WORKSPACE}
COPY ./docker/firebase/export-firebase.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/export-firebase.sh && \
  apk add --update --no-cache openjdk11-jre bash curl nodejs npm sudo &&\
  gcloud components install cloud-datastore-emulator beta --quiet && \
  echo "${CONTAINER_USER} ALL=NOPASSWD: ALL" > /etc/sudoers.d/${CONTAINER_USER} && \
  npm -g install firebase-tools && \
  chown -R ${CONTAINER_USER}:$(id ${CONTAINER_USER} -g -n) ${WORKSPACE}
USER cloudsdk
COPY ./docker/firebase/storage.rules .