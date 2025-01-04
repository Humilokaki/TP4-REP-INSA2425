ARG MY_PYTHON_VERSION=3.8

FROM python:${MY_PYTHON_VERSION}-slim

WORKDIR /app

ARG MY_PYTHON_VERSION
ARG WORKFLOW=default

ENV WORKFLOW=${WORKFLOW}

RUN echo "Python Version: ${MY_PYTHON_VERSION}"

COPY requirements_${MY_PYTHON_VERSION}.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && \
  python -m ipykernel install --user --name=python-container-env --display-name "Python ${PYTHON_VERSION} (Docker REP project)"

COPY . .

EXPOSE 8888

CMD ["bash", "-c", "\
  echo \"Starting the workflow\"; \
  if [ \"$WORKFLOW\" = \"replicate\" ]; then \
  echo \"Launching replicate command\"; \
  python scraping.py 2014 2024 && jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root; \
  elif [ \"$WORKFLOW\" = \"default\" ]; then \
  echo \"Launching reproducible command\"; \
  python scraping.py 2014 2020 && jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root; \
  else \
  echo \"Invalid workflow, please use either 'replicate' or 'default' with '-e WORKFLOW=replicate or default'\"; \
  fi; \
  "]


