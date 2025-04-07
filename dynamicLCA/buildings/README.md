## Dynamic life cycle assessment

This repository contains the dynamic life cycle assessment (LCA) codebase, input data, and output data in the paper 'Net-zero timber cities critically depend on proactive resource management' by Yayla et al. 

This study explores the long-term emissions/sinks and temperature rise in future cities under different forest/waste management scenarios, and it presents a novel dynamic LCA model coded in Python, which simulates the behaviour of the elementary flows during and after the lifespan of the buildings.

### Overview

This dynamic LCA model gives particular attention to the accurate modelling of urbanisation rate, CO<sub>2</sub> uptake from both biomass regrowth, carbonation of concrete, and destinations of building materials at end-of-life for future urban buildings. 

The code also calculates atmospheric GHG concentration changes, and life cycle impact assessment (LCIA) indicators: static and dynamic global warming potential (GWP) for different time horizons (20, 100, and 200 years), and absolute global temperature potential (AGTP).

The model was implemented in Python (v3.9.16). All input and output datasets are stored in the data repository hosted on<a href="https://doi.org/10.5281/zenodo.13886867" target="_blank" style=" text-decoration: none !important; color:red !important;"> Zenodo &#10140;</a>.

### System requirements

This dynamic LCA code requires only a standard computer with enough RAM to support the in-memory operations. The code has been tested on Microsoft Windows 11 Pro, x64-based processor, and 32.0 GB of installed RAM.

### Documentation and installation guide

- See Python documentation <a href="https://docs.python.org/3/" target="_blank" style=" text-decoration: none !important; color:red !important;">here &#10140;</a>
- See Jupyter Notebook documentation <a href="https://docs.jupyter.org/en/latest/" target="_blank" style=" text-decoration: none !important; color:red !important;">here &#10140;</a>

#### Python dependencies

```
numpy
pandas
scipy.stats
random
plotly
time
tqdm
os
```

### Instructions

The main analysis and plotting codes are stored in `/src`. Raw data are stored in `/raw_data`. The list of scenarios (building types, building numbers for regional analysis, and all other important parameters) can be built by running the `Jupyter Notebook` files in `/src/generating_scenario_data`, and these scenario data are stored in `/generated_data` to be used by `Main_dLCA.py`.

The main code loops through each building type. For each, it places the start-of-life and end-of-life emission pulse along a time series. Dynamic sinks (carbonation and forest regrowth) and emissions (landfill decay emissions) are also converted to a continuous series of pulses. These are then convoluted with greenhouse gas decay functions as defined by Joos et al.[^1] according to the method proposed by Cherubini et al.[^2]. A dynamic GWP indicator is then calculated based on the method by Ventura et al.[^3].  

Figures can be plotted using additional codes. Output data are returned to `/output/results`, and figures to `/output/figures`. Unless otherwise stated in the output data tables, GWP results are in kilograms of carbon dioxide equivalent (kg CO2-eq.) and AGTP results are in Kelvin (K).

### References

[^1]: Joos, F. et al. Carbon dioxide and climate impulse response functions for the computation of greenhouse gas metrics: a multi-model analysis. Atmos Chem Phys 13, 2793-2825 (2013). https://doi.org/10.5194/acp-13-2793-2013
[^2]: Cherubini, F., Peters, G. P., Berntsen, T., Stromman, A. H. & Hertwich, E. CO<sub>2</sub> emissions from biomass combustion for bioenergy: atmospheric decay and contribution to global warming. Gcb Bioenergy 3, 413-426 (2011). https://doi.org/10.1111/j.1757-1707.2011.01102.x
[^3]: Ventura, A. Conceptual issue of the dynamic GWP indicator and solution. Int J Life Cycle Ass 28, 788-799 (2023). https://doi.org/10.1007/s11367-022-02028-x