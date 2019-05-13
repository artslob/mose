FROM postgres:11.2

ENV entrypoint /docker-entrypoint-initdb.d/

RUN mkdir -p ${entrypoint}

ENV scripts /scripts/

WORKDIR $scripts

COPY db-scripts/recreate-db.sh $scripts
