FROM 119.3.170.97:5000/ubuntu
ADD . /usr/src
VOLUME /usr/src
WORKDIR /usr/src
RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple
CMD ./run.sh