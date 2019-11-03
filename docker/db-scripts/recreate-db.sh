#!/usr/bin/env bash

PGPASSWORD=wizuber_pass psql -U wizuber_user -d postgres -c 'DROP DATABASE "wizuber_db";';
PGPASSWORD=wizuber_pass psql -U wizuber_user -d postgres -c 'CREATE DATABASE "wizuber_db";';
