FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update

#RUN apt upgrade -y

RUN apt install tzdata -y

RUN ln -fs /usr/share/zoneinfo/America/Santiago /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

ENV TZ="America/Santiago"

RUN apt install openssl libssl-dev libbz2-dev libclang-dev git net-tools nano vim cmake curl locales g++ ca-certificates git wget vim meson software-properties-common libboost-dev libboost-all-dev -y

RUN apt install python3-dev -y 

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

#RUN apt install omniorb libomniorb4-dev omniorb-idl python-omniorb -y 

RUN apt install pip -y

RUN pip install zeroc-ice

RUN pip install ipython ipaddress


# Define working directory.
WORKDIR /home
RUN wget http://downloads.sourceforge.net/project/omniorb/omniORB/omniORB-4.3.0/omniORB-4.3.0.tar.bz2
RUN wget http://downloads.sourceforge.net/project/omniorb/omniORBpy/omniORBpy-4.3.0/omniORBpy-4.3.0.tar.bz2
RUN tar -xjvf omniORB-4.3.0.tar.bz2
RUN tar -xjvf omniORBpy-4.3.0.tar.bz2

RUN mkdir omniORB-4.3.0/build && cd omniORB-4.3.0/build && ../configure && make && make install
RUN mkdir omniORBpy-4.3.0/build && cd omniORBpy-4.3.0/build && ../configure --with-omniorb=/usr/local && make && make install
RUN echo "PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.8/site-package" >> /etc/bash.bashrc
RUN echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/" >> /etc/bash.bashrc


#WORKDIR /root

COPY dmc_source .

# Set environment variables.
ENV HOME /root
ENV PYTHONPATH $PYTHONPATH:/usr/local/lib/python3.8/site-packages
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/lib/

RUN mkdir /var/omninames

CMD ["omniNames", "-start" , "2809"]


#RUN python3 client.py