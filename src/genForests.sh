#!/bin/bash

#check args
if [ "$#" -ne 4 ]
then
    echo "Generates random forests to evaluate path planning"
    echo "Usage: $0 <number of worlds to gen> <world long length> <world side length> <tree density> "
    exit 1
fi

echo "generating worlds"
python3 random_forest_gen.py --num_worlds $1 --world_length $2 --world_width $3 --tree_density $4



echo "done"
