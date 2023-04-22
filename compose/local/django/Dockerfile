# syntax=docker/dockerfile:1

FROM python:3.10.5

# Don’t delete the downloaded apt packages
RUN rm -f /etc/apt/apt.conf.d/docker-clean

# Install apt packages, keep a cache
RUN  apt-get update && apt-get install -yqq --no-install-recommends \
  gettext && rm -rf /var/lib/apt/lists/*
