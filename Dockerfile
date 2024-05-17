FROM ubuntu:latest
LABEL authors="solomon"

ENTRYPOINT ["top", "-b"]