#!/bin/bash

export SVGA_VGPU10=0
source /ros_entrypoint.sh

if [ -d "Atividade_01/build" ]; then
    rm -rf Atividade_01/build
fi

if [ -d "Atividade_01/devel" ]; then
    rm -rf Atividade_01/devel
fi

cd Atividade_01 && catkin_make && cd ..

source Atividade_01/devel/setup.bash

rosdep update
rosdep install --from-paths Atividade_01/src --ignore-src -r -y --rosdistro noetic

roslaunch lar_gazebo lar_husky_script.launch