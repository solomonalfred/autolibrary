FROM python:3.9 AS base
WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim AS app
COPY --from=base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
WORKDIR /
COPY . .
ENTRYPOINT ["python3", "src/app.py"]