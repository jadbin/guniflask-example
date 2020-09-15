FROM python:3.7

ADD ./ /opt/guniflask_example
WORKDIR /opt/guniflask_example

RUN chmod +x bin/manage \
  && pip install -r requirements/app.txt

ENTRYPOINT ["bin/manage", "start", "--daemon-off"]
