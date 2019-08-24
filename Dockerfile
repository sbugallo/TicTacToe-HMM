FROM continuumio/miniconda3:4.7.10

LABEL maintainer="Sergio Bugallo <sergiobugalloenjamio@gmail.com>"

RUN mkdir /ttt
WORKDIR /ttt

COPY ./env.yml /ttt/env.yml
RUN conda env create -f /ttt/env.yml
RUN echo '. activate ttt' >> ~/.bashrc

COPY . /ttt
RUN bash -c '/opt/conda/envs/ttt/bin/python /ttt/setup.py install'

CMD [ "/bin/bash" ]