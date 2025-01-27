FROM jtbai/takuvik:ppv1_machine

WORKDIR /takuvik

ADD *.h ./
ADD *.hpp ./
ADD *.c ./
ADD *.cpp ./
ADD makefile_docker ./
RUN mv makefile_docker Makefile

ADD *.py ./
ADD *.i ./

ADD ./domain ./domain
ADD ./ui ./ui

RUN make
ENTRYPOINT ["python", "main.py"]