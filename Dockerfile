FROM continuumio/miniconda3:4.7.10

LABEL maintainer="Sergio Bugallo <sergiobugalloenjamio@gmail.com>"

RUN bash -c 'mkdir -p /ttt/envs'
WORKDIR /ttt

COPY ./envs/prod.yml /ttt/envs/prod.yml
RUN conda env create -f /ttt/envs/prod.yml
RUN echo '. activate ttt' >> ~/.bashrc

COPY . /ttt
RUN bash -c '/opt/conda/envs/ttt/bin/python /ttt/setup.py install'

CMD [ "/bin/bash" ]