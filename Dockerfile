FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        build-essential \
        python3.6 \
        python3.6-dev \
        python3-pip \
        python-setuptools \
        cmake \
        wget \
        curl \
        libsm6 \
        libxext6 \ 
        libxrender-dev

RUN python3.6 -m pip install -U pip
RUN python3.6 -m pip install --upgrade setuptools

COPY requirements.txt /tmp

WORKDIR /tmp

RUN python3.6 -m pip install -r requirements.txt

COPY . /coref_res

WORKDIR /coref_res

RUN chmod +x install.sh && ./install.sh


EXPOSE 50051

RUN mkdir -p /root/.allennlp/models/ && wget "https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz" -O /root/.allennlp/models/coref-model-2018.02.05.tar.gz

RUN python3.6 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Service/coref.proto

CMD ["python3.6", "start_service.py"]