FROM python:3.8
LABEL maintainer "Daeun Lee <storyda1@naver.com>"

RUN apt -y update && apt -y dist-upgrade
WORKDIR /Miraclenote
COPY . /Miraclenote
RUN apt install -y libsndfile1
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 manage.py makemigrations --settings=miraclenote.settings.local
RUN python3 manage.py migrate --settings=miraclenote.settings.local

EXPOSE 8000
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["--noreload", "--settings=miraclenote.settings.local"]
