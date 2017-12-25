FROM python:latest
ENV ME_ROOT /srv/tcztzy
RUN mkdir ${ME_ROOT}
WORKDIR ${ME_ROOT}
ADD requirements.txt ${ME_ROOT}
RUN pip install -r requirements.txt
ADD tcztzy ${ME_ROOT}/