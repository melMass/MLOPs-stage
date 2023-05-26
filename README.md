# MLOPS Stage
*Only for MLOPs 2.0+*

### SD from Scene

This high level node wraps the whole `Camera to Points` -> `Points to Mesh` pipeline

**features**:
- **Use multiparm for cameras**. A whole pipeline is created per camera. Each camera embeds its own settings and you can have per camera positive and negative prompts (on top of the global ones)  
![cameras_multiparm](help/images/sd_from_scene_01.png)

**random preview from development**
#### The demo file. This will show you how to split the output as everything gets merged

https://github.com/melMass/MLOPs-stage/assets/7041726/812ca29b-dc81-401f-a119-afcc4ea2ed47


#### previewing the 2D and projected points at the same time (not that MLOPs controlnet was broken back then)

https://github.com/melMass/MLOPs-stage/assets/7041726/756b265b-54d0-41f6-acb5-fb14a47aabd6


#### Attempt to transfer back to mesh (this is part of the demo file)

https://github.com/melMass/MLOPs-stage/assets/7041726/506fdfd1-78f1-48a8-99c6-c7799745a2b0


