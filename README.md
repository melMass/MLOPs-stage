# MLOPS Stage
*Only for MLOPs 2.0+*

## Nodes

### SD from Scene

This high level node wrap the whole `Camera to Points` -> `Points to Mesh` pipeline

**features**:
- Use multiparm for cameras. A whole pipeline is create per camera. Each camera embed their own settings and you can have per camera positive and negatives (on top of the global ones)
![cameras_multiparm](help/images/sd_from_scene_01.png)

**random preview from development**