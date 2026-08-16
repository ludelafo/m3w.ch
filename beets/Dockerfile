FROM python:3.13-slim AS build

ARG LIBKEYFINDER_VERSION=2.2.8
ARG KEYFINDER_CLI_VERSION=1.2.0

RUN apt-get update && apt-get install --no-install-recommends --yes \
    build-essential \
    ca-certificates \
    cmake \
    curl \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libfftw3-dev \
    libswresample-dev \
  && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL "https://github.com/mixxxdj/libkeyfinder/archive/refs/tags/${LIBKEYFINDER_VERSION}.tar.gz" | tar xz \
    && cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF \
      -S "libkeyfinder-${LIBKEYFINDER_VERSION}" -B build-libkeyfinder \
    && cmake --build build-libkeyfinder --parallel "$(nproc)" \
    && cmake --install build-libkeyfinder

RUN curl -fsSL "https://github.com/EvanPurkhiser/keyfinder-cli/archive/refs/tags/v${KEYFINDER_CLI_VERSION}.tar.gz" | tar xz \
    && cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_TESTING=OFF \
      -S "keyfinder-cli-${KEYFINDER_CLI_VERSION}" -B build-keyfinder-cli \
    && cmake --build build-keyfinder-cli --parallel "$(nproc)" \
    && cmake --install build-keyfinder-cli

FROM python:3.13-slim

# docker compose build --build-arg BEETS_SOURCE="beets[autobpm,chroma,discogs,fetchart,lastgenre,lyrics,replaygain,tidal,titlecase] @ git+https://github.com/ludelafo/beets-fork.git@fix-replaygain-metaflac-backend-altering-input-files"
ARG BEETS_VERSION=2.13.1
ARG BEETS_SOURCE="beets[autobpm,chroma,discogs,fetchart,lastgenre,lyrics,replaygain,tidal,titlecase]==${BEETS_VERSION}"
ARG BEETS_UID=1000
ARG BEETS_GID=1000

VOLUME ["/config", "/downloads", "/data"]

ENV BEETSDIR=/config

WORKDIR /config

RUN apt-get update && apt-get install --no-install-recommends --yes \
    build-essential \
    cmake \
    flac \
    ffmpeg \
    imagemagick \
    jpegoptim \
    git \
    libcairo2-dev \
    libchromaprint-tools \
    libgirepository-2.0 \
    lame \
    mp3val \
    opus-tools \
    python3-gi \
    gettext-base \
    rsgain \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid "${BEETS_GID}" beets \
    && useradd --uid "${BEETS_UID}" --gid beets --home-dir /config --no-create-home --shell /usr/sbin/nologin beets \
    && mkdir -p /config /downloads /data /etc/beets \
    && chown -R beets:beets /config /downloads /data /etc/beets

RUN pip install --no-cache-dir \
    "${BEETS_SOURCE}" \
    beets-filetote \
    beets-getlrc \
    pip-system-certs \
    pyxdg

COPY --from=build /usr/local/bin/keyfinder-cli /usr/local/bin/keyfinder-cli
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY convert.sh /usr/local/bin/convert.sh
COPY plugins/encode.py /usr/local/lib/beets-plugins/encode.py
COPY plugins/clean.py /usr/local/lib/beets-plugins/clean.py
COPY plugins/cover.py /usr/local/lib/beets-plugins/cover.py
COPY plugins/disambiginalbum.py /usr/local/lib/beets-plugins/disambiginalbum.py
# COPY plugins/replaygain.py /usr/local/lib/beets-plugins/replaygain.py
COPY plugins/tags.py /usr/local/lib/beets-plugins/tags.py
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/convert.sh

USER beets:beets
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["--help"]
