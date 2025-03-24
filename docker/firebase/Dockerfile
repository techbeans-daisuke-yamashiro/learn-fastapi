FROM google/cloud-sdk:alpine
WORKDIR /emulator
RUN apk add --update --no-cache openjdk11-jre bash curl nodejs npm &&\
  gcloud components install cloud-datastore-emulator beta --quiet
USER cloudsdk