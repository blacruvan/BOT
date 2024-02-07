FROM python:3.9-slim

COPY bot.py requirements.txt modules/taboas.py /

RUN pip install -r requirements.txt

CMD ['python', './bot.py'] 