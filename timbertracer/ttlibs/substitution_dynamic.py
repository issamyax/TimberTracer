


def substitution_factors_dynamic(ref_year, PH):
  """
  This function computes the dynamic substitution factors
  The dynamic_sub excel file contains the evolution of emissions by time + the referential substitution
  """
  df_emiss = pd.read_excel('dynamic_subs.xlsx')
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
