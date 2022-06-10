FROM ubuntu
WORKDIR /opt/app

COPY . .

#Install packages
RUN apt-get -y update && apt-get -y install software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt-get -y install python3.10 && apt-get -y install python3-pip

#Install supplied toncli version
RUN pip install -e ./toncli && cd ./bin && toncli update_libs

RUN pip install --no-cache-dir -r ./api/requirements-prod.txt

EXPOSE 5000

WORKDIR /opt/app/api

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
