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
5.  **Computational Notebook**: Access the [Google Colab Computational Notebook](https://colab.research.google.com/github/issamyax/TimberTracer/blob/main/TimberTracer_Usage%20TutorialV2.ipynb) that demonstrates the usage of the model, step-by-step analysis, and interpretation of results. [Google Colab Computational Notebook](https://colab.research.google.com/github/issamyax/TimberTracer/blob/main/TimberTracer_Usage%20TutorialV2.ipynb)

## References 

I. Boukhris, A. Collalti, S. Lahssini, D. Dalmonech, F. Nakhle, R. Testolin, M. V. Chiriacò, M. Santini, R. Valentini. TimberTracer: A Comprehensive Framework for the Evaluation of Carbon Sequestration by Forest Management and Substitution of Harvested Wood Products doi: https://doi.org/10.1101/2024.01.24.576985
