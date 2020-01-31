FROM python:3.6.1-alpine
RUN pip install flask
RUN pip install requests

RUN mkdir -p /opt/code
WORKDIR /opt/code
EXPOSE 80

CMD ["python","app.py"]
COPY app.py /opt/code/app.py
COPY templates /opt/code/templates
COPY static /opt/code/static
