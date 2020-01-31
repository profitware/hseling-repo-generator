FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN apt-add-repository universe
RUN apt-get update
RUN apt-get install python-pip -y
RUN pip install flask
RUN pip install json-rpc
RUN pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0rc0-cp27-none-linux_x86_64.whl

RUN mkdir -p /app/save
WORKDIR /app
EXPOSE 80

CMD ["python","app.py"]
COPY hseling_api_generator/save/ /app/save/
COPY hseling_api_generator/model.py /app/model.py
COPY hseling_api_generator/utils.py /app/utils.py
COPY hseling_api_generator/sample.py /app/sample.py
COPY hseling_api_generator/app.py /app/app.py
