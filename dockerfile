FROM mongo:latest

# Installer les outils MongoDB manuellement
RUN apt-get update && \
    apt-get install -y wget && \
    wget -qO- https://fastdl.mongodb.org/linux/mongodb-shell-linux-x86_64-ubuntu2004-6.0.5.tgz | tar -zxvf - && \
    mv mongodb-linux-x86_64-ubuntu2004-6.0.5/bin/mongo /usr/bin/mongo && \
    chmod +x /usr/bin/mongo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["mongod"]
