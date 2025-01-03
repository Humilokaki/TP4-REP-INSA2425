ARG MY_PYTHON_VERSION=3.8

FROM python:${MY_PYTHON_VERSION}-slim

WORKDIR /app

ARG MY_PYTHON_VERSION

RUN echo "Python Version: ${MY_PYTHON_VERSION}"

COPY requirements_${MY_PYTHON_VERSION}.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m ipykernel install --user --name=python-container-env --display-name "Python ${PYTHON_VERSION} (Docker REP project)"

COPY . .

EXPOSE 8888

ARG WORKFLOW=default

CMD ["bash", "-c", "\
  echo \"Starting the workflow\"; \
  echo \"WORKFLOW: $WORKFLOW, PYTHON_VERSION: $MY_PYTHON_VERSION\"; \
  python scraping.py 2014 2020 && jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root"]


