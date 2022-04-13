# SDVN-Optimization
Here, we tried to optimize the famous SDN problem which is a multi objectives problem with new metaheuristics like PSO, TLBO, VBO and so on.

## Install

In order to use this project, you'll need to install python 3. Once done, you'll have to install 2 libraries : _**matplotlib**_ and _**numpy**_

To install required dependencies please enter the following command in the root folder of the project
```
pip install -r requirements.txt
```

## Launch

Both metaheuristic algorithms TLBO and VBO are implemented in separated files _**TLBO.py**_ and _**VBO_Algorithm.py**_

To Visualise the results, launch the script _**test.py**_
```
python test.py
```

As a result, you should see the non-dominated particles for each algorithm. It should look like below

<p align="center">
<img src="5.png" width="80%"/>
 </p>
