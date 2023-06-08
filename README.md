# MLOPS Stage

> Warning!
> This is a community project not directly affiliated with MLOPs if some nodes become mature enough they will be proposed upstream but all this is mostly experimental!



*Only for MLOPs 2.0+* 

Sets of HDA Extension for the [MLOPS](https://github.com/Bismuth-Consultancy-BV/MLOPs) toolset from [@Bismuth-Consultancy-BV](https://www.bismuthconsultancy.com/) that I made while learning it. Moslty experimental and POC level for now. Other community members are starting to share tools to on the [Bismuth Discord Server](https://discord.gg/kYNaHt7Yx8)

Feel free to PR or propose suggestions

## Installation
I recommend the [package](https://www.sidefx.com/docs/houdini/ref/plugins.html) install method, ask if you have issues. 

- Clone this repo somewhere and note the path (`--recursive` will be probably be needed soon)
- Edit the [sample package file](./MLOPS_community.json) replacing the `path` value with yours.
- Restart Houdini.

  
## Nodes

### Scene to Controlnet

The heart or SD from Scene, this creates a strip of images from the given camera and objects, feeding them to ControlNet 1.1 (Depth or Normal supported for now). 

### SD From Scene

This high level node wraps the whole `Camera to Points` -> `Points to Mesh` pipeline

### DeepBump (soon™)

A simple deepbump integration for MLOPs, I still need to properly check all licenses involved, works well in combo with SD from Scene's generated texture maps.

### Camera To Points Simple

A small rework of the old camera to points by **#leuns3051** (450384314769735682).  
Mostly useful for embedding it in HDAs as older versions were removed, the current version in MLOPs is using editable parm making it hard to do that.
It misses the OGL render pass from the 2.0 version in MLOPs.




--- 

<details><summary>random previews from early tests</summary>

https://github.com/melMass/MLOPs-stage/assets/7041726/44ee5543-132a-4e39-ae3e-ad1b5ae1c733

https://github.com/melMass/MLOPs-stage/assets/7041726/41b1a371-497e-46aa-a138-417ff49b49ac

https://github.com/melMass/MLOPs-stage/assets/7041726/de49f854-bc1b-4a61-a061-ec86d48faaec

</details>