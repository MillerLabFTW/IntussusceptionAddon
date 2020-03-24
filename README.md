# Intussusception Add-on for Blender

Authored by Saarang Panchavati, Miller Lab, Rice University, July 2016 | Advisor: Jordan Miller

A [Blender](http://www.blender.org) add-on for generating Intussusception fractal vasculature for 3D printing and computational fluid dynamics simulations and modeling.

![MillerLab logo](Intussusception.png)


## Overview

Intussusception is the natural process by which one blood vessel splits into two.  This add-on is an attempt to model this process in order to create functional positive flow models for 3D vascular networks. We create fractal vasculature by starting with a single tube and sequentially, dichotomously dividing all available tubes with each fractal generation. 

Currently, this add-on allows the user to adjust the following parameters: 

Print-ready scaling, length, angle, number of divisions, reduction in branching distance, inlet/outlet, bounding box, narrowing, space filling, skin radius, and Murray’s Law implementation. 

## Documentation 

This git repository includes: The python file for the add-on, and explanatory videos. 

## Installation/Usage Instructions

1. First ensure you have downloaded and and installed the latest version of [Blender](https://www.blender.org/download/). This add-on has been developed and tested with `Blender 2.77a`.

1. Download this repository: [https://github.com/MillerLabFTW/IntussusceptionAddon/archive/master.zip](https://github.com/MillerLabFTW/IntussusceptionAddon/archive/master.zip)

1. Unzip the repository. You should find the required `IntusAddon.py` inside.

1. In Blender, navigate to `User Preferences > Add-ons > Install from File ` and find and select the `IntusAddon.py` file in this repository and activate it. Screenshots:

![UserPrefs](PicsVids/ShowUserPrefs.png)
![UserPrefs](PicsVids/UserPrefs-InstallFromFile.png)
![UserPrefs](PicsVids/IntusAddon-Selected.png)



1. Ensure it is checked in the add-on menu - It will be called `Add Mesh: Intussusception`

![UserPrefs](PicsVids/IntussusceptionSelected.png)


1. To use the add-on, in the 3D view window, type `<spacebar>` in the Blender Window and search for `Intussusception` in the pop-up.

![UserPrefs](PicsVids/Intussusception-Active.png)


1. You can adjust all the controls described above under `Overview`. To see what they will do, watch the video [`Intus-Addon-Display`](https://github.com/MillerLabFTW/IntussusceptionAddon/blob/master/PicsVids/Intus-Addon-Display.mov?raw=true) located in the `PicsVids` folder of this repository.

![UserPrefs](PicsVids/Intussusception-Example.png)

### Overview of Parameters
`Divisions` - Number of times the model divides

![UserPrefs](PicsVids/gifs/divisions.gif)


`Length` - Adjusts length of the model

![UserPrefs](PicsVids/gifs/length.gif)


`Angle` - Adjusts angle of initial branching

![UserPrefs](PicsVids/gifs/angle.gif)


`Reduction` - Adjusts amount by which the distance between branches decreases each division

![UserPrefs](PicsVids/gifs/reduction.gif)


`Inlet/Outlet` - Adds inlet and outlet to model

![UserPrefs](PicsVids/gifs/inout.gif)


`Bounding Box` - Adds bounding box to model 

![UserPrefs](PicsVids/gifs/bounding.gif)


`Print Ready` - Adjusts model and bounding box scaling to 34x14x11 dimensions

![UserPrefs](PicsVids/gifs/printReady.gif)


`2D Model` - Collapses Intussusception to 2 Dimensions

![UserPrefs](PicsVids/gifs/2d.gif)


`Narrow` - Moves back initial vertices to compact model, allowing minimal volume to be consumed by vasculature. 

![UserPrefs](PicsVids/gifs/narrow.gif)


`Spacefilling` - Moves groups of branches to be more space filling. Only works when `Narrow` is on.

![UserPrefs](PicsVids/gifs/spacefill.gif)


`Skin Radius` - Adjusts the radius of the skin modifier on all vertices

![UserPrefs](PicsVids/gifs/skinrad.gif)


### Murray’s Law

[Murray’s Law](https://en.wikipedia.org/wiki/Murray%27s_law) describes the relationship between a parent branch and its daughter branches wherein:
r<sup>3</sup><sub>p</sub> = r<sub>d<sub>1</sub></sub><sup>3</sup>+ r<sub>d<sub>2</sub></sub><sup>3</sup> + … + r<sub>d<sub>n</sub></sub><sup>3</sup>

`Murray’s Exponent` - Varies the exponent for Murray’s Law, which is generally 3

`Equal Murray’s Law` - Applies Murray’s Law on the model, assuming that all daughter branches have the same radius

![UserPrefs](PicsVids/gifs/emurray.gif)


`Random Murray’s Law` - Applies Murray’s Law on the model, but allows daughter branches to be of varying diameter 

![UserPrefs](PicsVids/gifs/rmurray.gif)



## Acknowledgements


![MillerLab logo](MillerLab_logo.jpg)
