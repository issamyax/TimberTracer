import config as ttdata
import scipy.stats as stats

def compute_R(n, r, init_stock, lifespan):
    """
    This function computes the annual recycling (for a period of n years) of a product, given its initial stock, recycling rate, and lifespan
    """
    # Distribution function of the decay
    distribution = stats.norm(lifespan, lifespan/3)
    R = [0]  # Initialize R[0] with the given value
    R.append(init_stock * (distribution.cdf(1) - distribution.cdf(0)) * r)  # Compute R[1]

    # This loop computes the annual recycling for the rest of the years (n-2)
    for i in range(3, n+1):
        term_sum = 0
        # Here the annual decay of recycling is computed
        for j in range(1, i):
            term_sum += R[j-1] * (distribution.cdf(i-j) - distribution.cdf(i-j-1))
        # Here we are adding the annual recycling to the decay of the initial stock
        R_i = term_sum * r + init_stock * (distribution.cdf(i-1) - distribution.cdf(i-2)) * r # i -> i-1 & i-1 -> i-2
        R.append(R_i)

    return R

def compute_D(n, r, init_stock, lifespan, k):
    """
    This function computes the annual production of landfill or firewood propotionally to the annual decay of the wood stock (k being the proportion)
    """
    # Distribution function of the decay
    distribution = stats.norm(lifespan, lifespan/3)
    D = [0] # Initialize D[0] with the given value
    R = [0] # Initialize R[0] with the given value
    D.append(init_stock*(distribution.cdf(1) - distribution.cdf(0))*k) # Compute D[1]
    R.append(init_stock * (distribution.cdf(1) - distribution.cdf(0)) * r) # Compute R[1]

    # This loop computes the annual wood decay for the remaining years (n-"")
    for i in range(3,n+1):
      term_sum = 0

      for j in range(1,i):
          term_sum += R[j-1] * (distribution.cdf(i-j) - distribution.cdf(i-j-1))

      R_i = term_sum * r + init_stock * (distribution.cdf(i-1) - distribution.cdf(i-2)) * r # i -> i-1 & i-1 -> i-2
      R.append(R_i)
      # Computing the annual production of landfill or firewood by multiplying the decay by the proportion k
      D_i = (term_sum + init_stock*(distribution.cdf(i-1) - distribution.cdf(i-2)))*k
      D.append(D_i)

    return D

def compute_S(r, init_stock, lifespan, n):
    """
    This function computes the annual stock of a given product given its initial stock, lifespan and recycling rate, during the period n
    """
    distribution = stats.norm(lifespan, lifespan/3)
    S = [init_stock]  # Initialize S[0] with the given value
    S.append(init_stock * (distribution.cdf(1) - distribution.cdf(0)) * r + init_stock * (1- distribution.cdf(1) ))  # Compute S[1]
    R = [0]  # Initialize R[0] with the given value
    R.append(init_stock * (distribution.cdf(1) - distribution.cdf(0)) * r)  # Compute R[1]

    # This loop computes the product stock for the remaining years (n-2)
    for i in range(3, n+1):
        term_sum = 0
        term_sum2 = 0
        for j in range(1, i):
            term_sum += R[j-1] * (distribution.cdf(i-j) - distribution.cdf(i-j-1))
            term_sum2 += R[j-1] * (1 - distribution.cdf(i-j))
        # Annual recycling computation
        R_i = term_sum * r + init_stock * (distribution.cdf(i-1) - distribution.cdf(i-2))*r
        R.append(R_i)
        # Adding the recycling to the total current stock composed from both the initial stock and the new stock which is constituted from recyclings
        S_i = R_i +   init_stock * (1 - distribution.cdf(i-1)) + term_sum2
        S.append(S_i)

    return S


def total_recycling_calculator(df, recycling_matrix, decay_matrix, n):
  """
  This function computes the total annual recycing of all the products given their proper use properties (Recycling rate, Lifespan)
  """
  result_list = []
  # Iterate through the DataFrame rows
  for index, row in df.iterrows():
      product = row['product']
      if product in recycling_matrix:
          r1 = recycling_matrix[product]['r']
          init_stock = row['post_process_volume']
          lifespan = recycling_matrix[product]['ls']
          result = compute_R(n, r1, init_stock, lifespan)
          result_list.append(result)

  # Sum the elements at corresponding positions in the lists
  sum_result = [sum(x) for x in zip(*result_list)]
  sum_result = [x*ttdata.K*ttdata.D*ttdata.CC*10 for x in sum_result] #10 just for the scale, to get the real results you must remove multiplication by 10

  return sum_result


def total_stock_calculator(df, recycling_matrix, decay_matrix, n):
    """
    This function computes the total annual stock including the product stock, the landfill stock, and the millsite stock
    """
    result_list = []
    result_list1 = []
    total_s = sum(df['post_process_volume'])* ttdata.K*ttdata.D*ttdata.CC

    # 1) Calculate the stock of landfill
    # Iterate through the DataFrame rows
    for index, row in df.iterrows():
        product = row['product']
        if product in recycling_matrix:
            r1 = recycling_matrix[product]['r']
            r2 = recycling_matrix[product]['landfill']
            init_stock = row['post_process_volume']
            lifespan = recycling_matrix[product]['ls']
            result1 = compute_D(n, r1, init_stock, lifespan, r2)
            result_list.append(result1)

    # Sum the elements at corresponding positions in the lists
    sum_result = [sum(x) for x in zip(*result_list)]

    # Create a normal distribution
    distribution = stats.norm(decay_matrix["landfill"], decay_matrix["landfill"]/3)

    # Initialize LF list with a 0 at index 0
    LF = [0]

    # Calculate LF values for indices 1 to n+1
    for i in range(2, n+1):
        termo = 0
        for j in range(1, i+1):
            termo += sum_result[j-1] * (1 - distribution.cdf(i-j))

        LF.append(termo)


    # 2) Calculate stock of millsite
    distribution_mill = stats.norm(decay_matrix["millsite"], decay_matrix["millsite"] / 3)
    millsite_init_value = df[df['product']== 'millsite']['post_process_volume'].iloc[0]
    MS = [millsite_init_value]
    for i in range(2,n+1):
      stock_i = millsite_init_value * (1 - distribution_mill.cdf(i-1))
      MS.append(stock_i)

    # 3) Calculate the stock in products
    # Iterate through the DataFrame rows
    for index, row in df.iterrows():
        product1 = row['product']
        if product1 in recycling_matrix:
            r1 = recycling_matrix[product1]['r']
            init_stock1 = row['post_process_volume']
            lifespan1 = recycling_matrix[product1]['ls']
            result1 = compute_S(r1, init_stock1, lifespan1, n)
            result_list1.append(result1)

    # Sum the elements at corresponding positions in the lists
    sum_result1 = [sum(x) for x in zip(*result_list1)]

    resultat = [sum(x) for x in zip(LF, MS, sum_result1)]
    resultat = [x*ttdata.K*ttdata.D*ttdata.CC for x in resultat] # K: Drying, D: Density, CC: Carbon content
    resultat[0] = total_s
    return resultat


def total_emission_calculator(df, recycling_matrix, decay_matrix, n):
  """
  This function computes the total emissions from firewood, landfill and, millsite
  """
  result_list = []
  result_list1 = []

  # 1) Compute emissions from landfill
  # Iterate through the DataFrame rows
  for index, row in df.iterrows():
      product = row['product']
      if product in recycling_matrix:
          r1 = recycling_matrix[product]['r']
          r2 = recycling_matrix[product]['landfill']
          init_stock = row['post_process_volume']
          lifespan = recycling_matrix[product]['ls']
          result1 = compute_D(n, r1, init_stock, lifespan, r2)
          result_list.append(result1)

  # Sum the elements at corresponding positions in the lists
  sum_result = [sum(x) for x in zip(*result_list)]

  # Create a normal distribution
  distribution = stats.norm(decay_matrix["landfill"], decay_matrix["landfill"] / 3)

  LFE = [0,0]
  # Calculate LF values for indices 3 to n
  for i in range(3, n+1):
    termo = 0
    for j in range(2, i):
      termo += sum_result[j-1] * (distribution.cdf(i-j) - distribution.cdf(i-j-1))
    LFE.append(termo)

  # 2) Compute emissions from fire
  # Iterate through the DataFrame rows
  for index, row in df.iterrows():
      product1 = row['product']
      if product1 in recycling_matrix:
          r1 = recycling_matrix[product1]['r']
          r2 = recycling_matrix[product1]['fire']
          init_stock1 = row['post_process_volume']
          lifespan1 = recycling_matrix[product1]['ls']
          result2 = compute_D(n, r1, init_stock1, lifespan1, r2)
          result_list1.append(result2)

  # Sum the elements at corresponding positions in the lists
  sum_result1 = [sum(x) for x in zip(*result_list1)]
  sum_result1[0] = df[df['product']== 'fire']['post_process_volume'].iloc[0]

  # Create a normal distribution
  distribution1 = stats.norm(decay_matrix["fire"], decay_matrix["fire"] / 3)

  FRE = [0]
  # Calculate FRE values for indices 2 to n
  for i in range(2, n+1):
    termo = 0
    for j in range(1, i):
      termo += sum_result1[j-1] * (distribution1.cdf(i-j) - distribution1.cdf(i-j-1))
    FRE.append(termo)

  # 3) Compute emissions from millsite
  MSE = [0]
  distribution_mill = stats.norm(decay_matrix["millsite"], decay_matrix["millsite"] / 3)
  millsite_init_value = df[df['product']== 'millsite']['post_process_volume'].iloc[0]
  for i in range(2,n+1):
    stock_i = millsite_init_value * (distribution_mill.cdf(i-1)- distribution_mill.cdf(i-2))
    MSE.append(stock_i)

  #return MSE
  resultat = [sum(x) for x in zip(LFE, FRE, MSE)]
  resultat =[x*ttdata.K*ttdata.D*ttdata.CC for x in resultat] # K: drying, D: Density, CC: Carbon content
  return resultat