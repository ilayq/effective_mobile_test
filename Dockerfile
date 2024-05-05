FROM python:3.12-alpine


COPY . .
RUN python3 -m unittest
CMD ["python3", "main.py"]
