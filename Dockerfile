#./Dockerfile
FROM python:3 
#기반이 될 이미지
    
WORKDIR ./
# 작업디렉토리(default)설정
    
## Install packages
COPY requirements.txt ./ 
#현재 패키지 설치 정보를 도커 이미지에 복사

RUN pip install -r requirements.txt 
#설치정보를 읽어 들여서 패키지를 설치
    
## Copy all src files
COPY . .
## Run the application on the port 8080
EXPOSE 5000   

    
#CMD ["python", "./setup.py", "runserver", "--host=0.0.0.0", "-p 8080"]
CMD ["python3", "manage.py"]

