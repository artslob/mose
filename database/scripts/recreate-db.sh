#!/usr/bin/env bash

PGPASSWORD=secret_pass psql -U user -d postgres -c 'DROP DATABASE "wizuber";';
PGPASSWORD=secret_pass psql -U user -d postgres -c 'CREATE DATABASE "wizuber";';
