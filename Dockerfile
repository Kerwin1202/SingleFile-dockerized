FROM buildkite/puppeteer

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4EB27DB2A3B88B8B

RUN apt-get update \
     && apt-get install -y git

RUN npm install 'gildas-lormeau/SingleFile#master'

WORKDIR /opt/app

RUN apt-get update && apt-get install --no-install-recommends -y \
      python3 python3-pip python3-setuptools

COPY requirements.txt .

RUN pip3 install \
    --no-cache-dir \
    --no-warn-script-location \
    --user \
    -r requirements.txt

RUN rm requirements.txt

COPY webserver.py .

ENTRYPOINT ["/node_modules/single-file/cli/single-file", "--browser-executable-path=/opt/google/chrome/google-chrome", "--browser-args='[\"--no-sandbox\"]'", "--dump-content"]
