FROM python:latest
ENV ME_ROOT /srv/me
RUN mkdir ${ME_ROOT}
WORKDIR ${ME_ROOT}
ADD requirements.txt ${ME_ROOT}/
RUN pip install -r requirements.txt
ADD . ${ME_ROOT}/