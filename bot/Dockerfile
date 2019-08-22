FROM python:3.7.4

COPY requirements.txt requirements.txt
COPY bot.py bot.py
COPY bot_utils/ bot_utils
COPY generator/ generator/
COPY orm/ orm/
COPY trained_data/ trained_data/

RUN pip install -r requirements.txt

CMD ["python", "run_bot.py"]