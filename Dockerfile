### BASE STAGE ###

# Build from ros dev box
FROM jgkawell/ros:base AS base

# Needed for NLP audio packages
RUN apt -y update && apt -y install \
        python-catkin-tools \
        portaudio19-dev \
        gcc \
        g++

# Create catkin workspace
RUN mkdir -p ~/catkin_ws/src
RUN /bin/bash -c '. /opt/ros/kinetic/setup.bash; cd ~/catkin_ws/; catkin build'


# Clone CAIRO NLP
COPY . /root/catkin_ws/src/cairo-nlp

# Install Python requirements
RUN cd ~/catkin_ws/src/cairo-nlp && pip install -r requirements.txt

# Current workaround since Google Cloud installation is broken
RUN pip install --upgrade pip
RUN pip install --upgrade 'setuptools<45.0.0'
RUN pip install --upgrade 'cachetools<5.0'
RUN pip install --upgrade cryptography
RUN python -m easy_install --upgrade pyOpenSSL

# Finally build the workspace
RUN cd ~/catkin_ws && catkin build

# Source the workspace with each new terminal
RUN echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc

# Clean up apt
RUN rm -rf /var/lib/apt/lists/*

### NVIDIA STAGE ###

# Extra needed setup for Nvidia-based graphics
FROM base AS nvidia

# Copy over needed OpenGL files from Nvidia's image
COPY --from=nvidia/opengl:1.0-glvnd-runtime-ubuntu16.04 /usr/local /usr/local
COPY --from=nvidia/opengl:1.0-glvnd-runtime-ubuntu16.04 /etc/ld.so.conf.d/glvnd.conf /etc/ld.so.conf.d/glvnd.conf
