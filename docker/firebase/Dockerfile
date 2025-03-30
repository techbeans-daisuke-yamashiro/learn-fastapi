FROM google/cloud-sdk:alpine
ARG CONTAINER_USER=cloudsdk
ARG WORKSPACE=/opt/firebase
WORKDIR ${WORKSPACE}
RUN apk add --update --no-cache openjdk11-jre bash curl nodejs npm sudo &&\
  gcloud components install cloud-datastore-emulator beta --quiet && \
  echo "${CONTAINER_USER} ALL=NOPASSWD: ALL" > /etc/sudoers.d/${CONTAINER_USER} && \
  npm -g install firebase-tools 
  COPY  --chown=${CONTAINER_USER}:${CONTAINER_USER} ./docker/firebase/crontab /var/spool/cron/crontabs/${CONTAINER_USER}
  USER cloudsdk
  RUN sudo chown -R ${CONTAINER_USER}:${CONTAINER_USER} ${WORKSPACE}