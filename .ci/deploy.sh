#!/usr/bin/env bash

set -e

MOSE_PROJECT="/home/artslob/mose-project"
SOURCES="${MOSE_PROJECT}/sources"

PG_DB_VERSION="11.5"
PG_DB="postgresql-${PG_DB_VERSION}"
PG_DB_SOURCE="${SOURCES}/${PG_DB}"
PG_DB_TAR="${PG_DB_SOURCE}.tar.gz"
PG_DB_TARGET="${MOSE_PROJECT}/${PG_DB}"
PG_DB_DATA="${MOSE_PROJECT}/pgdata"
PG_DB_LOG_DIR="${MOSE_PROJECT}/pglog"
PG_DB_LOG="${PG_DB_LOG_DIR}/logfile.log"

PG_CONFIGURED="${PG_DB_SOURCE}-configured"
PG_MADE="${PG_DB_SOURCE}-made"
PG_MADE_INSTALLED="${PG_DB_SOURCE}-made-installed"

mkdir -p "$SOURCES"

if [[ ! -f "$PG_DB_TAR" ]]; then
    wget -nv "https://ftp.postgresql.org/pub/source/v${PG_DB_VERSION}/${PG_DB}.tar.gz" --no-check-certificate -O "$PG_DB_TAR"
fi

if [[ ! -d "$PG_DB_SOURCE" ]]; then
    gzip -dc "$PG_DB_TAR" | tar -C "$SOURCES" -xf -
fi

mkdir -p "$PG_DB_TARGET"

cd "$PG_DB_SOURCE"
if [[ ! -f "$PG_CONFIGURED" ]]; then
    "${PG_DB_SOURCE}/configure" --prefix="$PG_DB_TARGET" --without-readline > /dev/null
    touch "$PG_CONFIGURED"
fi
if [[ ! -f "$PG_MADE" ]]; then
    make --directory "$PG_DB_SOURCE" > /dev/null
    touch "$PG_MADE"
fi
if [[ ! -f "$PG_MADE_INSTALLED" ]]; then
    make --directory "$PG_DB_SOURCE" install > /dev/null
    touch "$PG_MADE_INSTALLED"
fi
if [[ ! -d "$PG_DB_DATA" ]]; then
    "${PG_DB_TARGET}/bin/initdb" -D "$PG_DB_DATA" -U postgres
fi

sed -i '/port = \d*/c\port = 57122' "${PG_DB_DATA}/postgresql.conf"
egrep 'port = \d*' "${PG_DB_DATA}/postgresql.conf"
mkdir -p "$PG_DB_LOG_DIR"
