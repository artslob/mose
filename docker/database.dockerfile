FROM postgres:11.5

ENV entrypoint /docker-entrypoint-initdb.d/

RUN mkdir -p ${entrypoint}

ENV scripts /scripts/

WORKDIR $scripts

COPY db-scripts/recreate-db.sh $scripts
