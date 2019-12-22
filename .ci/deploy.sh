#!/usr/bin/env bash

set -e
set -o xtrace

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

PYTHON_VERSION="3.6.8"
PYTHON="Python-${PYTHON_VERSION}"
PYTHON_SOURCE="${SOURCES}/${PYTHON}"
PYTHON_TAR="${PYTHON_SOURCE}.tar.gz"
PYTHON_TARGET="${MOSE_PROJECT}/${PYTHON}"
PYTHON_VENV="${MOSE_PROJECT}/venv"

PYTHON_CONFIGURED="${PYTHON_SOURCE}-configured"
PYTHON_MADE="${PYTHON_SOURCE}-made"
PYTHON_MADE_INSTALLED="${PYTHON_SOURCE}-made-installed"
PYTHON_VENV_CREATED="${PYTHON_SOURCE}-venv-created"

mkdir -p "$SOURCES"

if [[ ! -f "$PYTHON_TAR" ]]; then
    wget -nv "https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON}.tgz" --no-check-certificate -O "$PYTHON_TAR"
fi

if [[ ! -d "$PYTHON_SOURCE" ]]; then
    gzip -dc "$PYTHON_TAR" | tar -C "$SOURCES" -xf -
fi

mkdir -p "$PYTHON_TARGET"

cd "$PYTHON_SOURCE"
if [[ ! -f "$PYTHON_CONFIGURED" ]]; then
    "${PYTHON_SOURCE}/configure" --prefix="$PYTHON_TARGET" > /dev/null
    touch "$PYTHON_CONFIGURED"
fi
if [[ ! -f "$PYTHON_MADE" ]]; then
    make --directory "$PYTHON_SOURCE" > /dev/null
    touch "$PYTHON_MADE"
fi
if [[ ! -f "$PYTHON_MADE_INSTALLED" ]]; then
    make --directory "$PYTHON_SOURCE" install > /dev/null
    touch "$PYTHON_MADE_INSTALLED"
fi

"${PYTHON_TARGET}/bin/python3" --version

if [[ ! -f "$PYTHON_VENV_CREATED" ]]; then
    "${PYTHON_TARGET}/bin/python3" -m venv "$PYTHON_VENV"
    touch "$PYTHON_VENV_CREATED"
fi

"${PYTHON_VENV}/bin/python3" -m pip install --upgrade pip setuptools

if [[ -f "${MOSE_PROJECT}/mose/requirements.txt" ]]; then
    "${PYTHON_VENV}/bin/python3" -m pip install -r "${MOSE_PROJECT}/mose/requirements.txt"
fi
