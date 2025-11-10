FROM mcr.microsoft.com/devcontainers/base:ubuntu

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Définit bash comme shell par défaut
SHELL ["/bin/bash", "-c"]

USER vscode
WORKDIR /workspaces/tolid.io_sleeplab_Health

# Ajoute une commande de démarrage
CMD ["/bin/bash"]
