FROM osrf/ros:noetic-desktop-full
RUN apt update && apt clean
RUN apt install -y ros-noetic-hector-slam ros-noetic-husky-gazebo ros-noetic-husky-desktop ros-noetic-plotjuggler-ros && apt clean
RUN apt install -qqy x11-apps && apt clean
RUN apt install -y ros-noetic-husky-navigation ros-noetic-tf2-tools && apt clean

RUN export uid=1000 gid=1000
RUN mkdir -p /home/docker_user
RUN echo "docker_user:x:${uid}:${gid}:docker_user,,,:/home/docker_user:/bin/bash" >> /etc/passwd
RUN echo "docker_user:x:${uid}:" >> /etc/group
RUN echo "docker_user ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/docker_user
RUN chmod 0440 /etc/sudoers.d/docker_user
RUN chown ${uid}:${gid} -R /home/docker_user

USER docker_user
ENV HOME /home/docker_user
CMD ["bash"]