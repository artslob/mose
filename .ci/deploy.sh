#!/usr/bin/env bash

set -e

MOSE_PROJECT="/home/artslob/mose-project"
PG_DB_VERSION="11.5"
PG_DB="postgresql-${PG_DB_VERSION}"
SOURCES="${MOSE_PROJECT}/sources"
PG_DB_SOURCE="${SOURCES}/${PG_DB}"
PG_DB_TAR="${PG_DB_SOURCE}.tar.gz"

mkdir -p "$SOURCES"

if [ ! -f "$PG_DB_TAR" ]; then
    wget -nv "https://ftp.postgresql.org/pub/source/v${PG_DB_VERSION}/${PG_DB}.tar.gz" --no-check-certificate -O "$PG_DB_TAR"
fi

if [ ! -d "$PG_DB_SOURCE" ]; then
    gzip -dc "$PG_DB_TAR" | tar -C "$SOURCES" -xf -
fi

