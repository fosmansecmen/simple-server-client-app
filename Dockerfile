FROM python:3.7-alpine
WORKDIR /opt/lana
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY * ./
CMD python server.py