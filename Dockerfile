FROM python

MAINTAINER harry.kodden@surfnet.nl

# Prepare image with prequisites...

RUN apt-get update
RUN apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev vim

# Prepare Python prequisites...

ADD requirements.txt .
RUN pip install -r requirements.txt

# Prepare Application area...

WORKDIR /usr/local/src
ADD app.py .

# Run Application !

CMD ["python", "app.py"]