# Forest Generator for Gazebo
Random forest generator with using different type of bushes and trees to create test enviroment for Gazebo


![Image](https://github.com/user-attachments/assets/d16ecc90-65d5-4f80-b0a5-61c37339aaac)
Random forest enviroment for the test SLAM or path planner etc. algorithm.


Based on 
https://github.com/ethz-asl/forest_gen
```
@inproceedings{oleynikova2016continuous-time,
  author={Oleynikova, Helen and Burri, Michael and Taylor, Zachary  and  Nieto, Juan and Siegwart, Roland and Galceran, Enric},
  booktitle={IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  title={Continuous-Time Trajectory Optimization for Online UAV Replanning},a
  year={2016}
}
```
This is improvement version of this repository and adapted for Ros Noetic and Gazebo 11.

For trees and bushes https://github.com/kubja/gazebo-vegetation is used

You can create forest and test with ROS the world you created.

Featues:

- Changable Width and Length of Map
- Changable Tree density
- Changable Bush and Tree Type
- Changable percentage of the bush and tree type (%10 Tree_1, %20 Tree_2 ...)
- Better Distribution for Tree distribution

Required:
```
pip3 install pyDOE
pip3 install numpy=1.21
pip3 install scipy=1.7.0
```

To generate world:

```
cd src
./genForests.sh (number of random world) (map length) (map width) (tree density)
./genForests.sh 10 50 50 0.1
```
So basically it will create 10 different world file with 0.1 tree density and forest size will be 50 x 50 m.

You can also change the bush and tree type in the python file random_forest_gen.py

In line 188-191 you can use tree model which you want and you can adjust the percentage.
same for bushes line 246
```
#numbers =[1,2,3,4,5,6,7,9] % available tree models
#weights = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.3]
numbers =[1,3,2,9]  #tree model which you want to use
weights = [0.1,0.1,0.4,0.4] # percentage of the tree model tree 1-> %10 tree 2-> %10 tree 2-> %40 tree 9-> %40 total should be 1
```

You can test your generated world in gazebo 
```
catkin build
source devel/setup.bash

roslaunch sim_gazebo forest.launch
```

In launch file check the world name because your generated world file will be inside of
"forest_gen --> src --> worlds --> gen_world"  folder
```
<arg name="world" default="$(find sim_gazebo)/worlds/forest0.world" />
```

To use world file in your workspace do not forget the copy paste "model" folder.


Additionally, instead of generating trees in the Random Forest using purely random sampling, I employed the Halton sequence to create a more uniformly distributed set of samples. This quasi-random sequence ensures that the trees are better spread out across the feature space, avoiding clustering and underrepresented regions that may occur with standard random sampling. As a result, this structured diversity among trees is expected to lead to more stable and representative simulations, especially in scenarios where uniform coverage of the input space is important.

![image](https://github.com/user-attachments/assets/d9dd2ef2-df15-40ec-8651-b137f3461599)
