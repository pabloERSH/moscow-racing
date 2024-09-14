FROM python: 3.12.5


SHELL ["/bin/bash", "-c"]


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD python3 -m daphne -p 8666 -b 0.0.0.0 moscowracing.asgi:application
