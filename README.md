# dynamic-LCA
## Overview

This code is used to performed a comparative dynamic life cycle analysis of two equivalent buildings made of reinforced concrete or engineered timber. 

It was developped for the following study: *Dynamic LCA of reinforced concrete and engineered timber buildings: special focus on carbonation and biogenic carbon* Yayla et al (unpublished)

## Disclaimer
The module is still in development.

## The code

The main analysis and plotting codes are stored in `/src`
To run the main analysis, the list of scenarios (building types and other important parameters sensitivity analysis) must be built by running the `Scenario_builder.py` code which treats LCI data in `/raw_data` into a format usable by `Main_dLCA.py`.

The main code loops through each building types. For each it places start and end of life emission pulse along a time series. Dynamic sinks (carbonation, forest regrowth) and emissions (lanfill decay emissions) are also converted to a continuous series of pulses. These are then convoluted with GHG decay functions as defined by Joos et al[^1] according to the method proposed by Cherubini et al[^2]. A dynamic GWP indicator is then calculated based on the Ventura et al's method[^3].  

Figures can be plotted using additional codes.

Outputs data are returned to `/Outputs`, and figures to `/figures`

## References
[^1]: Joos, F. et al. Carbon dioxide and climate impulse response functions for the computation of greenhouse gas metrics: a multi-model analysis. *Atmos Chem Phys 13, 2793-2825 (2013). https://doi.org/10.5194/acp-13-2793-2013
[^2]: Cherubini, F., Peters, G. P., Berntsen, T., Strømman, A. H. & Hertwich, E. CO2 emissions from biomass combustion for bioenergy: atmospheric decay and contribution to global warming. *Gcb Bioenergy* 3, 413-426 (2011). 
[^3]: Ventura, A. Conceptual issue of the dynamic GWP indicator and solution. *Int J Life Cycle Ass* 28, 788-799 (2023). https://doi.org/10.1007/s11367-022-02028-x
