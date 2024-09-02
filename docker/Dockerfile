FROM python:3.11

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

# # Instaling playwright
# RUN pip install playwright==1.46.0
# RUN playwright install
# RUN playwright install-deps

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./README.md ./
COPY ./LICENSE.txt ./
COPY ./pyproject.toml ./
RUN pip install .[lint,test] --no-deps
COPY ./tests ./tests

RUN chmod -R a+x .