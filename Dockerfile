FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m ipykernel install --user --name=python-container-env --display-name "Python 3.8 (Docker REP project)"

COPY . .

EXPOSE 8888

CMD ["bash", "-c", "python scraping.py && jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root"]
