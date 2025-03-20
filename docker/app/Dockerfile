FROM python:3.12-slim as installer
ARG CONTAINER_USER
ARG CONTAINER_UID
ARG CONTAINER_GID
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo
COPY ./src/pyproject.toml /tmp
COPY ./docker/app/startup.sh /usr/local/bin/
RUN apt update && apt upgrade -y && pip install --upgrade pip && \
  apt -y install tzdata ca-certificates build-essential libmariadb-dev pkg-config sudo && apt clean &&\
  adduser -u ${CONTAINER_UID} ${CONTAINER_USER} && \
  echo "${CONTAINER_USER} ALL=NOPASSWD: ALL" > /etc/sudoers.d/${CONTAINER_USER} && \
  pip install poetry && poetry config virtualenvs.create false && \
  cd /tmp && poetry install && sudo chmod +x /usr/local/bin/startup.sh
WORKDIR /app
USER ${CONTAINER_USER}

  
# デプロイ用
# FROM python:3.12-slim AS main
# COPY --from=installer /usr/local/lib/python3.12/site-packages  /usr/local/lib/python3.12/site-packages
CMD ["/usr/local/bin/startup.sh"]
EXPOSE 8000