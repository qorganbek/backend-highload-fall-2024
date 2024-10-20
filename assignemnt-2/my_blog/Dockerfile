FROM python:3.11-slim



WORKDIR /my_blog


COPY requirements.txt /my_blog/
RUN pip install --no-cache-dir -r requirements.txt


COPY . /my_blog//


EXPOSE 8000

