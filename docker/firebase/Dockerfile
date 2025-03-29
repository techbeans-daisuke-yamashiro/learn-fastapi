FROM google/cloud-sdk:alpine
ARG CONTAINER_USER=cloudsdk
WORKDIR /opt/firebase
RUN apk add --update --no-cache openjdk11-jre bash curl nodejs npm sudo &&\
  gcloud components install cloud-datastore-emulator beta --quiet && \
  echo "${CONTAINER_USER} ALL=NOPASSWD: ALL" > /etc/sudoers.d/${CONTAINER_USER} && \
  npm -g install firebase-tools 
USER cloudsdk