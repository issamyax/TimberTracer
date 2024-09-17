# TimberTracer: A Comprehensive Framework for the Evaluation of Carbon Sequestration by Forest Management and Substitution of Harvested Wood Products.

<p align="center">
  <img src="logo.png"  align="center" width="400" height="250" >
</p>

## Overview

This Python-based model offers a comprehensive analysis of wood products, emphasizing the factors influencing carbon pools, emissions, and the temporal dynamics associated with harvested wood products. Its primary goal is to provide insights into both carbon sequestration and emissions over time. For more information, please refer to the preprint published at https://doi.org/10.1101/2024.01.24.576985

The Model exists in two versions. The upgrade from Version 1 to Version 2 adressed two important considerations. The new version accounts for the methane release from landfills and enable a dynamic computation of substitution factors proportionnaly to GHG emissions in line with the Paris agreement in climate change. 

## Features

- **Carbon Sequestration Analysis**: Assess the amount of carbon stored in various wood products.
- **Emission Dynamics**: Understand the emissions associated with different stages of wood product utilization.
- **Substitution effect**: Evaluate the substitution of fossil fuel and energy-intensive materials.
- **Temporal Insights**: Examine how carbon sequestration and emissions evolve over time.
- **Modular Design**: Easily extend or modify components to adapt to specific research needs.

## Requirements

- Python 3.x
- Additional libraries listed in requirements.txt

## Installation

1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd timbertracer/
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1.  **Configuration**: Modify the variables in the `config.py` file to customize the analysis parameters according to your requirements.
2.  **Data Preparation**: Ensure your wood product data is formatted according to the provided examples. TimberTracer can be seamlessly coupled with any forest growth model, whether individual-tree or stand-based level, such as Go+ (Moreaux et al., 2020) or 3DCMCC-FEM (Collalti et al., 2014).

3.  **Data Input**: Modify `__main.py__` to include your parameters in the `app.run_model()` function for the Version 1 or `app_new.run_model()` for the Version 2. 
4.  **Run the Model**: Execute the main script to initiate the analysis: `bash python main.py`
5.  **Computational Notebook**: Access the [Google Colab Computational Notebook](https://colab.research.google.com/github/issamyax/TimberTracer/blob/main/TimberTracer_Usage%20TutorialV2.ipynb) that demonstrates the usage of the model, step-by-step analysis, and interpretation of results. [![Google Colab Computational Notebook](https://colab.research.google.com/github/issamyax/TimberTracer/blob/main/TimberTracer_Usage%20TutorialV2.ipynb)

## References 

1. Alessio Collalti, Lucia Perugini, Monia Santini, Tommaso Chiti, Angelo Nolè, Giorgio Matteucci, Riccardo Valentini, A process-based model to simulate growth in forests with complex structure: Evaluation and use of 3D-CMCC Forest Ecosystem Model in a deciduous forest in Central Italy, Ecological Modelling, Volume 272, 2014, Pages 362-378, ISSN 0304-3800, https://doi.org/10.1016/j.ecolmodel.2013.09.016.

2. Moreaux, V., Martel, S., Bosc, A., Picart, D., Achat, D., Moisy, C., Aussenac, R., Chipeaux, C., Bonnefond, J.-M., Figuères, S., Trichet, P., Vezy, R., Badeau, V., Longdoz, B., Granier, A., Roupsard, O., Nicolas, M., Pilegaard, K., Matteucci, G., … Loustau, D. (2020). Energy, water and carbon exchanges in managed forest ecosystems: Description, sensitivity analysis and evaluation of the INRAE GO+ model, version 3.0. Geoscientific Model Development, 13(12), 5973–6009. https://doi.org/10.5194/gmd-13-5973-2020
