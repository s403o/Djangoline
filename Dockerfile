FROM public.ecr.aws/docker/library/python:3.12-slim-bookworm

LABEL maintainer="Eslam Adel <eslam.adel.me@gmail.com>"

WORKDIR /home/semo/djangoline

ARG DEBIAN_FRONTEND="noninteractive"
# build packages
ARG BPKGS="git gcc curl"
# runtime packages
ARG RPKGS="libpq-dev python3-dev default-libmysqlclient-dev libpq5 libc6-dev"
# purge packages
ARG PPKGS="perl-base linux-libc-dev"

RUN --mount=type=cache,target=/var/cache/apt \
	apt-get update -yqq && apt-get upgrade -yqq && \
	apt-get --no-install-recommends install -yqq ${BPKGS} ${RPKGS} && \
	rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir --upgrade setuptools && \
    pip install pip-tools

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
	pip-sync && \
	apt-get autoremove -yqq --purge --allow-remove-essential ${BPKGS} ${PPKGS}

ARG GIT_COMMIT
ENV DJANGOLINE_GIT_COMMIT=$GIT_COMMIT

EXPOSE 8000

COPY . .