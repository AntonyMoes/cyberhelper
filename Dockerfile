FROM python:3.7.4

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]