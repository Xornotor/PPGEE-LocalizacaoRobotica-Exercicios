#!/bin/bash

export SVGA_VGPU10=0
source ./ros_entrypoint.sh

if [ -d "Atividade_02/build" ]; then
    rm -rf Atividade_02/build
fi

if [ -d "Atividade_02/devel" ]; then
    rm -rf Atividade_02/devel
fi

cd Atividade_02 && catkin_make && cd ..

source Atividade_02/devel/setup.bash
source Atividade_02/src/husky_accessories.sh

rosdep update
rosdep install --from-paths Atividade_02/src --ignore-src -r -y --rosdistro noetic

roslaunch lar_gazebo lar_husky_amcl.launch