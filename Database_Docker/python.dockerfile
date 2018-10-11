FROM python:3

WORKDIR /usr/src/app

COPY python_requirements.txt ./
RUN pip install --no-cache-dir -r python_requirements.txt

COPY /scripts/ /scripts/
WORKDIR /scripts/

ENTRYPOINT ["/bin/bash", "start.sh"]