FROM eoranged/rq-dashboard:latest

RUN pip install -U rq==1.10.1

ENV RQ_DASHBOARD_REDIS_URL=redis://:REDIS_PASS@db.gtdb.ecogenomic.org
