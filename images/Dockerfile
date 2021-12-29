FROM ubuntu:20.04

RUN apt update && apt install python3 -y && apt-get install -y libgl1-mesa-dev
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6

RUN apt install python3-pip -y  && pip install -U pip

RUN python3 -m pip install --upgrade pip
RUN pip3 --version
RUN pip install cmake
RUN pip install dlib
RUN pip3 install opencv_contrib_python && pip3 install PyQt5
RUN pip3 install opencv-python-headless==4.5.5.62 && pip3 install numpy && pip install face_recognition && pip3 install scipy
RUN apt install sqlite3 -y
