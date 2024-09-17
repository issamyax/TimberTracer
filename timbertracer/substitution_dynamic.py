import scipy.stats as stats
from ttlibs.recycling import compute_D, compute_R
import config as ttdata


def substitution_factors_dynamic(ref_year, PH):
  """
  This function computes the dynamic substitution factors
  The dynamic_sub excel file contains the evolution of emissions by time + the referential substitution
  """
  df_emiss = pd.read_excel(ttdata.dynamic_subs_file)
  substitution_ref = df_emiss[['furniture', 'lumber', 'sawing', 'particle', 'fire']].iloc[0].to_dict()
  df_ref = df_emiss[['year', 'emiss']]

  # Filter the dataframe for the specified period
  df_ref2 = df_ref[(df_ref['year'] >= ref_year) & (df_ref['year'] <= (ref_year + PH))].reset_index(drop=True)

  # Handle the case when the period extends beyond the available emission data
  if (ref_year + PH) > df_ref['year'].max():
    # Append additional rows with extrapolated years and placeholder emissions (initially same as the last known year)
    additional_years = pd.DataFrame({
        'year': range(df_ref['year'].max() + 1, ref_year + PH + 1),
        'emiss': df_ref['emiss'].iloc[-1]  # Placeholder, to be updated with extrapolation
    })
    df_ref2 = pd.concat([df_ref2, additional_years]).reset_index(drop=True) # concatenation of available emissions with extrapolated ones

  # Empty dictionary to store dynamic substitution values
  substitution_over_time = {}

  # Substitution initialization
  previous_year_substitution_values = substitution_ref.copy()

  # First year emission
  previous_year_emissions_values = df_ref2.iloc[0]['emiss']

  # First year substitution in dictionary
  substitution_over_time[df_ref2.iloc[0]['year']] = previous_year_substitution_values

  # Loop through the dataframe
  for index in range(1, len(df_ref2)):
      year = df_ref2.iloc[index]['year']
      if year <= df_ref['year'].max():
          current_emissions = df_ref2.iloc[index]['emiss']
          change = (current_emissions - previous_year_emissions_values) / previous_year_emissions_values
      else:
          # Use the last known change for years beyond the data # basically the change within the year 2100
          change = (df_ref['emiss'].iloc[-1] - df_ref['emiss'].iloc[-2]) / df_ref['emiss'].iloc[-2]
          current_emissions = previous_year_emissions_values * (1 + change)
          df_ref2.at[index, 'emiss'] = current_emissions  # Update the placeholder emissions

      # Calculate the current substitution values
      current_substitution = {product: previous_value * (1 + change) for product, previous_value in previous_year_substitution_values.items()}
      substitution_over_time[year] = current_substitution

      # Update for the next iteration
      previous_year_substitution_values = current_substitution
      previous_year_emissions_values = current_emissions

  # Convert dictionary to a dataframe
  substitution_df = pd.DataFrame(substitution_over_time).transpose().round(3)
  substitution_df = substitution_df.reset_index(names = 'year')

  return substitution_df


def energy_sub_dynamic(df, recycling_matrix, substitution_df, decay_matrix, C_CO2, n, K): # n will be affected PP+1 because by definition years = period +1
  """
  This function computes the annual dynamic energy substitution
  """
  result_list1 = []
  SEF = substitution_df['fire']
  #SEF = substitution_matrix['fire']
  # rendering columns from substitution_df => [year|emiss|furniture|lumber|sawing|particle|fire]
  listo = substitution_df.columns.tolist()
  # Iterate through the DataFrame rows
  for index, row in df.iterrows():
      product1 = row['product']
      filtered_substitution_matrix = [x for x in listo if x not in ['year', 'emiss', 'fire']]
      if product1 in filtered_substitution_matrix:
          r1 = recycling_matrix[product1]['r']
          r2 = recycling_matrix[product1]['fire']
          init_stock1 = row['post_process_volume']*K #K drying
          lifespan1 = recycling_matrix[product1]['ls']
          result2 = compute_D(n, r1, init_stock1, lifespan1, r2)
          result_list1.append(result2)

  # Sum the elements at corresponding positions in the lists
  sum_result1 = [sum(x) for x in zip(*result_list1)]
  sum_result1[0] = df[df['product']== 'fire']['post_process_volume'].iloc[0]


  # Create a normal distribution
  distribution1 = stats.norm(decay_matrix["fire"], decay_matrix["fire"] / 3)

  FRE = [0]
  # Calculate FRE values for indices 2 to (n+1)
  for i in range(2, n+1):
    termo = 0
    for j in range(1, i):
      termo += sum_result1[j-1] * (distribution1.cdf(i-j) - distribution1.cdf(i-j-1))
    FRE.append(termo)

  # Multiply the emissions from wood combustion by the time-corresponding substitution factor
  FRE = [a * b / C_CO2 for a, b in zip(SEF, FRE)]  # SEF: Substitution for Energy, C_CO2: C to CO2 conversion factor
  return FRE

def material_sub_dynamic(df, recycling_matrix, substitution_df, decay_matrix, C_CO2, n):
  """
  This function computes the annual dynamic material substitution
  """
  result_list1 = []
  # rendering columns from substitution_df => [year|emiss|furniture|lumber|sawing|particle|fire]
  listo = substitution_df.columns.tolist()
  # Iterate through the DataFrame rows
  for index, row in df.iterrows():
      product1 = row['product']
      filtered_substitution_matrix = [x for x in listo if x not in ['year', 'emiss', 'fire']]
      if product1 in filtered_substitution_matrix:
          SMF = substitution_df[product1] # material substitution factor for this product
          r1 = recycling_matrix[product1]['r']
          #SC = filtered_substitution_matrix[product1] # To suppress
          init_stock1 = row['post_process_volume']*K # K drying
          lifespan1 = recycling_matrix[product1]['ls']
          result2 = compute_R(n, r1, init_stock1, lifespan1)
          result2[0] = init_stock1 # the direct product of the stem in the first position
          result2 = [a * b  for a, b in zip(SMF, result2)] # multiplying by the DF - here the SMF is a product-specific displacement factor and has to be updated during each iteration (product)
          result_list1.append(result2)

  sum_result1 = [sum(x) for x in zip(*result_list1)] # summation of substitutions from all products
  sum_result1 = [x/C_CO2 for x in sum_result1]

  return sum_result1
