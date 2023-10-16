FROM mcr.microsoft.com/playwright/python:v1.34.0-jammy


WORKDIR /app


COPY actions /app/actions
COPY tests /app/tests
COPY utils /app/utils
COPY resources /app/resources
COPY conftest.py /app/
COPY definitions.py /app/
COPY pytest.ini /app/


COPY requirements.txt /app/

ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV HEADLESS 0
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps
