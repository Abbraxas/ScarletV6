
FROM nikolaik/python-nodejs:python3.10-nodejs19

RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i '/security.debian.org/d' /etc/apt/sources.list && \
    rm -f /etc/apt/sources.list.d/yarn.list \
          /etc/apt/sources.list.d/yarn.sources && \
    apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg aria2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/

COPY . /app/

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["bash", "start"]
