FROM almalinux/9-base:9.7-20260330

RUN dnf -y install epel-release && \
    dnf -y update && \
    dnf -y install python3.13 && \
    dnf clean all

WORKDIR /app

COPY app/ /app/

RUN chmod +x /app/manifest.py

ENTRYPOINT [ "python3.13", "/app/manifest.py" ]