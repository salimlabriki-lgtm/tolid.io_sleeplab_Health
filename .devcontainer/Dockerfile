FROM mcr.microsoft.com/devcontainers/base:ubuntu

# (Optionnel) Installe ce dont tu as besoin globalement dans l'env de dev
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# User par défaut dans Codespaces
USER vscode

WORKDIR /workspaces/tolid.io_sleeplab_Health
