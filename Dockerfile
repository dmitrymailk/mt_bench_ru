FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && apt-get install \
	git curl numactl wget libmpich-dev python3-dev \
	openmpi-bin openmpi-common openmpi-doc libopenmpi-dev \
	ffmpeg libsm6 libxext6 tree -y

ENV MPICC=/opt/ompi/bin/mpicc
ENV MPICXX=/opt/ompi/bin/mpicxx
RUN CC=${MPICC} pip install mpi4py==3.1.5

ARG USERNAME=user-name-goes-here
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
	&& useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
	#
	# [Optional] Add sudo support. Omit if you don't need to install software after connecting.
	&& apt-get update \
	&& apt-get install -y sudo \
	&& echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
	&& chmod 0440 /etc/sudoers.d/$USERNAME

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
RUN  echo -e "\nexport PATH=$PATH:/home/$USERNAME/.local/bin\n" >>  /home/$USERNAME/.bashrc && sudo chown -R $USERNAME /opt/conda

WORKDIR /code