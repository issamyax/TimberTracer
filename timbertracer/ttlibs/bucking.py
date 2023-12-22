import math
import numpy as np
import pandas as pd

def taper_equation(z, a1, a2, b1, b2, b3, b4):
    """
    This is the implementation of Max and Burkhart Equation
    z = 1 - hx/ht & dr2 = (dx/DBH)**2
    dx = sqrt(dr2)*DBH
    """
    dr2 = b1 * z + b2 * z ** 2 + b3 * (z > a1) * (z - a1) ** 2 + b4 * (z > a2) * (z - a2) ** 2
    return dr2

def knotted_wood_profile2(z, ht, a1, a2, b1, b2, b3, b4, a, c, alpha, beta):
    """
    This function dress the crown base profile of a tree making it possible to split profile into knotted and intact wood
    This function call 3 other functions : i-taper equation ii-crown base height iii-relation between dbh and ht
    This function will be used for the computation of knotted wood diameter
    Make sure in the plotting that zmin >= a and hc <= a*ht**c
    If zmin <a return taper diameter instead
    """
    # z = 1- hc/ht
    hc = (1-z)*ht
    zc = 1 - a*(hc**(c-1))
    dc = np.sqrt(taper_equation(zc, a1, a2, b1, b2, b3, b4))*alpha*((hc/a)**(1/c))**(beta)
    dx = np.sqrt(taper_equation(z, a1, a2, b1, b2, b3, b4))*alpha*(ht)**(beta)
    condition = 1 - a * (ht ** (c - 1))
    condition_check = z > condition
    return np.where(condition_check, dc, dx)

def sapwood_heartwood(dbh, DBH, sap_area, heart_area):
    """
    This function compute the sapwood width of a tree by leveraging the sapwood and heartwood areas provided by the growth model
    dbh is not the mean of the stand but the individual.
    DBH is the mean diameter
    """
    sap_width = math.sqrt(4/math.pi*(sap_area+heart_area)) - math.sqrt(4/math.pi*heart_area)
    sap_width = sap_width*dbh/DBH
    return sap_width

def sapwood_profile(z, a1, a2, b1, b2, b3, b4, bark, sap_area, heart_area, ht, dbh, DBH):
    """
    Although this function is titled sapwood, it computes the heartwood profile
    This is done by retrieving bark and sapwdidth which are considered fix along the stem
    """
    e = bark + sapwood_heartwood(dbh, DBH, sap_area, heart_area)
    dr2 = b1 * z + b2 * z ** 2 + b3 * (z > a1) * (z - a1) ** 2 + b4 * (z > a2) * (z - a2) ** 2
    dx = np.sqrt(dr2)*dbh
    dx = dx - e
    if dx > 0:
        return dx
    else:
        return 0

def knotted_to_sap(z, a1, a2, b1, b2, b3, b4, bark, ht, a, c, alpha, beta, dbh, DBH, sap_area, heart_area):
    """
    This function computes the ratio of knotted wood to heart wood along the stem
    """
    diameter_sap = sapwood_profile(z,a1,a2,b1,b2,b3,b4,bark,sap_area,heart_area, ht, dbh, DBH)
    diameter_knotted = knotted_wood_profile2(z,ht,a1,a2,b1,b2,b3,b4,a,c,alpha,beta)
    ratio = (diameter_knotted/diameter_sap)**2
    return ratio

def knotted_to_taper(z, ht, a1, a2, b1, b2, b3, b4, a, c, alpha, beta, dbh):
    """
    This function computes the ratio of knotted wood to stem along the stem
    """
    diameter_taper = np.sqrt(taper_equation(z, a1, a2, b1, b2, b3, b4))*dbh
    diameter_knotted = knotted_wood_profile2(z, ht, a1, a2, b1, b2, b3, b4, a, c, alpha, beta)
    ratio = diameter_knotted / diameter_taper
    return ratio

def find_h_above_threshold(threshold, a1, a2, b1, b2, b3, b4, tolerance):
    """
    This function is the implementation of the bisection method (Dichotomie in French)
    This function makes it possible to compute the value of x for a given f(x)
    In our case we compute the height level which satisfy diameter condition
    """
    lower_bound = 0
    upper_bound = 1

    max_iterations = 100
    iterations = 0

    while iterations < max_iterations:
        x = (lower_bound + upper_bound) /2
        y = taper_equation(x, a1, a2, b1, b2, b3, b4)

        if y > threshold:
            upper_bound = x
        else:
            lower_bound = x

        if abs(y - threshold) < tolerance:
            return x

        iterations +=1

        print(iterations)

    return None

def find_h_above_knotted_to_hw(threshold, a1, a2, b1, b2, b3, b4, bark, ht, a, c, alpha, beta, dbh, DBH, sap_area, heart_area, tolerance):
    """
    This function is the implementation of the bisection method (Dichotomie in French)
    This makes it possible to compute the value of x for a given f(x)
    In this case we compute the height level which satisfy the ratio knotted wood to heartwood
    """
    lower_bound = 0
    upper_bound = 1

    max_iterations = 100
    iterations = 0

    while iterations < max_iterations:
        x = (lower_bound + upper_bound) / 2
        y = knotted_to_sap(x,a1, a2, b1, b2, b3, b4, bark, ht, a, c, alpha, beta, dbh, DBH, sap_area, heart_area)

        if y > threshold:
            lower_bound = x
        else:
            upper_bound = x

        if abs(y - threshold) < tolerance:
            return x

        iterations += 1

        print(iterations)

    return None

def find_h_above_knotted_to_diam(threshold, ht, a1, a2, b1, b2, b3, b4, a, c, alpha, beta, dbh, tolerance):
    """
    This function is the implementation of the bisection method (Dichotomie in French)
    This makes it possible to compute the value of x for a given f(x)
    In this case we compute the height level which satisfy the ratio knotted wood to taper
    """
    lower_bound = 0
    upper_bound = 1

    max_iterations = 100
    iterations = 0

    while iterations < max_iterations:
        x = (lower_bound + upper_bound) / 2
        y = knotted_to_taper(x,ht, a1, a2, b1, b2, b3, b4, a, c, alpha, beta, dbh)

        if y > threshold:
            lower_bound = x
        else:
            upper_bound = x

        if abs(y - threshold) < tolerance:
            return x

        iterations += 1

        print(iterations)

    return None

def volume_calculator(start_height, end_height, dbh, ht, a1, a2, b1, b2, b3, b4):
    """
    This function compute the volume within the stem between two defined heights
    start_height stands for lower height and end_height stands for the upper height
    """
    k = math.pi/40000
    zy = 1 - start_height/ht
    zx = 1 - end_height/ht
    volume = k * (dbh**2) * ht * (b1/2 * (zy**2 - zx**2) +
             b2/2 * (zy**3 - zx**3) + b3/3 * ((zy - a1)**3 * (zy > a1) -
             (zx - a1)**3 * (zx > a1))  + b4/3 * ((zy - a2)**3 * (zy > a2) -
             (zx - a2)**3 * (zx > a2)))

    return volume



def bucking_allocation(dbh, ht, a1, a2, b1, b2, b3, b4, bark, a, c, alpha, beta, DBH, sap_area, heart_area, tolerance):

  # here is a definition of tresholds
  threshold7 = (7/dbh)**2
  threshold25 = (25/dbh)**2
  threshold_kw_hw = 0.13
  threshold_kw_diam = 0.3

  # here is a computation of the heights corresponding to those thresholds
  h7 = (1-find_h_above_threshold(threshold7, a1, a2, b1, b2, b3, b4, tolerance))*ht
  h25_calculations = find_h_above_threshold(threshold25, a1, a2, b1, b2, b3, b4, tolerance)
  #h25 = (1-find_h_above_threshold(threshold25, a1, a2, b1, b2, b3, b4, tolerance))*ht
  h25 = None if h25_calculations is None else (1 - h25_calculations)*ht
  h_kw_hw = (1-find_h_above_knotted_to_hw(threshold_kw_hw, a1, a2, b1, b2, b3, b4, bark, ht, a, c, alpha, beta, dbh, DBH, sap_area, heart_area, tolerance))*ht
  h_kw_diam = (1-find_h_above_knotted_to_diam(threshold_kw_diam, ht, a1, a2, b1, b2, b3, b4, a, c, alpha, beta, dbh, tolerance))*ht

  # First product : Stump
  stump = {'product': "Stump", "number": 1, "length": 0.3, "option1": 0.3, "option2": "", "start_height": 0,
             "end_height": 0.3}

  if h25 is None:
    h1 = 0
    h2 = 0
    h3 = 0
    furniture = {'product': "furniture", 'number': 0, "length": 0, 'option1': 0,
                    'option2': 0, "start_height": 0.3, "end_height": 0}
    lumber = {"product": "lumber", 'number': 0, "length": 0, 'option1': 0,
                'option2': 0, "start_height": 0, "end_height": 0}
    sawing = {"product": "sawing", 'number': 0, "length": 0, 'option1': 0,
                'option2': 0, 'start_height': 0, "end_height": 0}

  else:
      # Second product : Furniture
      d1 = min(h25,h_kw_hw) - 0.3
      quot1, remain1 = divmod(d1,5)
      if remain1 >= 3:
          h1 = quot1*5 + remain1
      else:
          h1 = quot1*5
      furniture = {'product': "furniture", 'number': quot1 + (remain1 >= 3)*1, "length": h1, 'option1': 5,
                    'option2': (remain1 >= 3)*remain1, "start_height": 0.3, "end_height": 0.3 + h1}

      # Third product : Lumber
      d2 = min(h25, h_kw_diam) - (0.3 + h1)
      quot2, remain2 = divmod(d2, 6)
      if remain2 >= 3:
          h2 = quot2*6 + remain2
      else:
          h2 = quot2*6
      lumber = {"product": "lumber", 'number': quot2 + (remain2 >= 3)*1, "length": h2, 'option1': 6,
                'option2': (remain2 >= 3)*remain2, "start_height": 0.3 + h1, "end_height": 0.3 + h1 + h2}

      # Fourth product : Sawing
      d3 = h25 - (0.3 + h1 + h2)
      quot3, remain3 = divmod(d3, 5)
      if remain3 >= 3:
          h3 = quot3*5 + remain3
      else:
          h3 = quot3*5
      sawing = {"product": "sawing", 'number': quot3 + (remain3 >= 3)*1, "length": h3, 'option1': 5,
                'option2': (remain3 >= 3)*remain3, 'start_height': 0.3 + h1 + h2, "end_height": 0.3 + h1 + h2 + h3}


  # Fifth product : Particle boards
  d4 = h7 - (0.3 + h1 + h2 + h3)
  quot4, remain4 = divmod(d4, 2.2)
  if quot4 >= 3:
      h4 = 3*2.2
  elif remain4 >= 2:
      h4 = quot4*2.2 + remain4
  else:
      h4 = quot4*2.2
  particle = {"product": "particle", 'number': quot4 + (quot4 < 3)*(remain4 >= 2)*1, "length": h4, 'option1': 2.2,
              'option2': (quot4 < 3)*(remain4 >= 2)*remain4, 'start_height': 0.3 + h1 + h2 + h3,
              "end_height": 0.3 + h1 + h2 + h3 + h4}

  # Sixth product : Paper pulp
  d5 = h7 - (0.3 + h1 + h2 + h3 + h4)
  quot5, remain5 = divmod(d5, 4.8)
  if remain5 >= 2.4:
      h5 = quot5*4.8 + remain5
  else:
      h5 = quot5*4.8
  paper = {"product": "paper", 'number': quot5 + (remain5 >= 2.4)*1, "length": h5, 'option1': 4.8,
            'option2': (remain5 >= 2.4)*remain5, 'start_height': 0.3 + h1 + h2 + h3 + h4,
            "end_height": 0.3 + h1 + h2 + h3 + h4 + h5}

  # Seventh product : Firewood
  d6 = h7 - (0.3 + h1 + h2 + h3 + h4 + h5)
  quot6, remain6 = divmod(d6, 1)
  if remain6 >= 0.5:
      h6 = quot6 * 1 + remain6
  else:
      h6 = quot6 * 1
  fire = {"product": "fire", 'number': quot6 + (remain6 >= 0.5) * 1, "length": h6, 'option1': 1,
          'option2': (remain6 >= 0.5) * remain6, 'start_height': 0.3 + h1 + h2 + h3 + h4 + h5,
          "end_height": 0.3 + h1 + h2 + h3 + h4 + h5 + h6}

  # Eight product: Toplog
  toplog = {"product": "toplog", 'number' : 1, 'length': ht - (0.3 + h1 + h2 + h3 + h4 + h5 + h6), "option1": "",
            "option2": "", 'start_height': 0.3 + h1 + h2 + h3 + h4 + h5 + h6,
            "end_height": ht}

  dico = [stump, furniture, lumber, sawing, particle, paper, fire, toplog]
  df = pd.DataFrame.from_dict(dico)
  df = df[df['number'] > 0]
  df['volume'] = df.apply(lambda row: volume_calculator(row['start_height'], row['end_height'],dbh, ht, a1, a2, b1, b2, b3, b4), axis = 1)

  return df


def bucking_allocation1(dbh, ht, a1, a2, b1, b2, b3, b4, bark, a, c, alpha, beta, DBH, sap_area, heart_area, tolerance):

  # here is a definition of tresholds
  threshold7 = (7/dbh)**2
  threshold25 = (25/dbh)**2
  threshold_kw_hw = 0.13
  threshold_kw_diam = 0.3

  # here is a computation of the heights corresponding to those thresholds
  h7 = (1-find_h_above_threshold(threshold7, a1, a2, b1, b2, b3, b4, tolerance))*ht
  h25 = (1-find_h_above_threshold(threshold25, a1, a2, b1, b2, b3, b4, tolerance))*ht
  h_kw_hw = (1-find_h_above_knotted_to_hw(threshold_kw_hw, a1, a2, b1, b2, b3, b4, bark, ht, a, c, alpha, beta, dbh, DBH, sap_area, heart_area, tolerance))*ht
  h_kw_diam = (1-find_h_above_knotted_to_diam(threshold_kw_diam, ht, a1, a2, b1, b2, b3, b4, a, c, alpha, beta, dbh, tolerance))*ht

  # First product : Stump
  stump = {'product': "Stump", "number": 1, "length": 0.3, "option1": 0.3, "option2": "", "start_height": 0,
             "end_height": 0.3}


  # Second product : Furniture
  d1 = min(h25,h_kw_hw) - 0.3
  quot1, remain1 = divmod(d1,5)
  if remain1 >= 3:
      h1 = quot1*5 + remain1
  else:
      h1 = quot1*5
  furniture = {'product': "furniture", 'number': quot1 + (remain1 >= 3)*1, "length": h1, 'option1': 5,
                'option2': (remain1 >= 3)*remain1, "start_height": 0.3, "end_height": 0.3 + h1}

  # Third product : Lumber
  d2 = min(h25, h_kw_diam) - (0.3 + h1)
  quot2, remain2 = divmod(d2, 6)
  if remain2 >= 3:
      h2 = quot2*6 + remain2
  else:
      h2 = quot2*6
  lumber = {"product": "lumber", 'number': quot2 + (remain2 >= 3)*1, "length": h2, 'option1': 6,
            'option2': (remain2 >= 3)*remain2, "start_height": 0.3 + h1, "end_height": 0.3 + h1 + h2}

  # Fourth product : Sawing
  d3 = h25 - (0.3 + h1 + h2)
  quot3, remain3 = divmod(d3, 5)
  if remain3 >= 3:
      h3 = quot3*5 + remain3
  else:
      h3 = quot3*5
  sawing = {"product": "sawing", 'number': quot3 + (remain3 >= 3)*1, "length": h3, 'option1': 5,
            'option2': (remain3 >= 3)*remain3, 'start_height': 0.3 + h1 + h2, "end_height": 0.3 + h1 + h2 + h3}

  # Fifth product : Particle boards
  d4 = h7 - (0.3 + h1 + h2 + h3)
  quot4, remain4 = divmod(d4, 2.2)
  if quot4 >= 3:
      h4 = 3*2.2
  elif remain4 >= 2:
      h4 = quot4*2.2 + remain4
  else:
      h4 = quot4*2.2
  particle = {"product": "particle", 'number': quot4 + (quot4 < 3)*(remain4 >= 2)*1, "length": h4, 'option1': 2.2,
              'option2': (quot4 < 3)*(remain4 >= 2)*remain4, 'start_height': 0.3 + h1 + h2 + h3,
              "end_height": 0.3 + h1 + h2 + h3 + h4}

  # Sixth product : Paper pulp
  d5 = h7 - (0.3 + h1 + h2 + h3 + h4)
  quot5, remain5 = divmod(d5, 4.8)
  if remain5 >= 2.4:
      h5 = quot5*4.8 + remain3
  else:
      h5 = quot5*4.8
  paper = {"product": "paper", 'number': quot5 + (remain5 >= 2.4)*1, "length": h5, 'option1': 4.8,
            'option2': (remain5 >= 2.4)*remain5, 'start_height': 0.3 + h1 + h2 + h3 + h4,
            "end_height": 0.3 + h1 + h2 + h3 + h4 + h5}

  # Seventh product : Firewood
  d6 = h7 - (0.3 + h1 + h2 + h3 + h4 + h5)
  quot6, remain6 = divmod(d6, 1)
  if remain6 >= 0.5:
      h6 = quot6 * 1 + remain6
  else:
      h6 = quot6 * 1
  fire = {"product": "fire", 'number': quot6 + (remain6 >= 0.5) * 1, "length": h6, 'option1': 1,
          'option2': (remain6 >= 0.5) * remain6, 'start_height': 0.3 + h1 + h2 + h3 + h4 + h5,
          "end_height": 0.3 + h1 + h2 + h3 + h4 + h5 + h6}

  # Eight product: Toplog
  toplog = {"product": "toplog", 'number' : 1, 'length': ht - (0.3 + h1 + h2 + h3 + h4 + h5 + h6), "option1": "",
            "option2": "", 'start_height': 0.3 + h1 + h2 + h3 + h4 + h5 + h6,
            "end_height": ht}

  dico = [stump, furniture, lumber, sawing, particle, paper, fire, toplog]
  df = pd.DataFrame.from_dict(dico)
  df = df[df['number'] > 0]
  df['volume'] = df.apply(lambda row: volume_calculator(row['start_height'], row['end_height'],dbh, ht, a1, a2, b1, b2, b3, b4), axis = 1)

  return df



def bucking_allocation2(dbh, ht, a1, a2, b1, b2, b3, b4, bark, a, c, alpha, beta, DBH, sap_area, heart_area, tolerance):

  # here is a definition of tresholds
  threshold7 = (7/dbh)**2
  threshold25 = (25/dbh)**2
  threshold_kw_hw = 0.13
  threshold_kw_diam = 0.3

  # here is a computation of the heights corresponding to those thresholds
  h7 = (1-find_h_above_threshold(threshold7, a1, a2, b1, b2, b3, b4, tolerance))*ht
  h25_calculations = find_h_above_threshold(threshold25, a1, a2, b1, b2, b3, b4, tolerance)
  #h25 = (1-find_h_above_threshold(threshold25, a1, a2, b1, b2, b3, b4, tolerance))*ht
  h25 = None if h25_calculations is None else (1 - h25_calculations)*ht
  h_kw_hw = (1-find_h_above_knotted_to_hw(threshold_kw_hw, a1, a2, b1, b2, b3, b4, bark, ht, a, c, alpha, beta, dbh, DBH, sap_area, heart_area, tolerance))*ht
  h_kw_diam = (1-find_h_above_knotted_to_diam(threshold_kw_diam, ht, a1, a2, b1, b2, b3, b4, a, c, alpha, beta, dbh, tolerance))*ht

  # First product : Stump
  stump = {'product': "Stump", "number": 1, "length": 0.3, "option1": 0.3, "option2": "", "start_height": 0,
             "end_height": 0.3}

  if h25 is None:
    h1 = 0
    h2 = 0
    h3 = 0
    furniture = {'product': "furniture", 'number': 0, "length": 0, 'option1': 0,
                    'option2': 0, "start_height": 0.3, "end_height": 0}
    lumber = {"product": "lumber", 'number': 0, "length": 0, 'option1': 0,
                'option2': 0, "start_height": 0, "end_height": 0}
    sawing = {"product": "sawing", 'number': 0, "length": 0, 'option1': 0,
                'option2': 0, 'start_height': 0, "end_height": 0}


  else:
      # Second product : Furniture
      d1 = min(h25,h_kw_hw) - 0.3
      quot1, remain1 = divmod(d1,5)
      if remain1 >= 3:
          h1 = quot1*5 + remain1
      else:
          h1 = quot1*5
      furniture = {'product': "furniture", 'number': quot1 + (remain1 >= 3)*1, "length": h1, 'option1': 5,
                    'option2': (remain1 >= 3)*remain1, "start_height": 0.3, "end_height": 0.3 + h1}

      # Third product : Lumber
      d2 = min(h25, h_kw_diam) - (0.3 + h1)
      quot2, remain2 = divmod(d2, 6)
      if remain2 >= 3:
          h2 = quot2*6 + remain2
      else:
          h2 = quot2*6
      lumber = {"product": "lumber", 'number': quot2 + (remain2 >= 3)*1, "length": h2, 'option1': 6,
                'option2': (remain2 >= 3)*remain2, "start_height": 0.3 + h1, "end_height": 0.3 + h1 + h2}

      # Fourth product : Sawing
      d3 = h25 - (0.3 + h1 + h2)
      quot3, remain3 = divmod(d3, 5)
      if remain3 >= 3:
          h3 = quot3*5 + remain3
      else:
          h3 = quot3*5
      sawing = {"product": "sawing", 'number': quot3 + (remain3 >= 3)*1, "length": h3, 'option1': 5,
                'option2': (remain3 >= 3)*remain3, 'start_height': 0.3 + h1 + h2, "end_height": 0.3 + h1 + h2 + h3}


  # Fifth product : Particle boards
  d4 = h7 - (0.3 + h1 + h2 + h3)
  quot4, remain4 = divmod(d4, 2.2)
  if quot4 >= 3:
      h4 = 3*2.2
  elif remain4 >= 2:
      h4 = quot4*2.2 + remain4
  else:
      h4 = quot4*2.2
  particle = {"product": "particle", 'number': quot4 + (quot4 < 3)*(remain4 >= 2)*1, "length": h4, 'option1': 2.2,
              'option2': (quot4 < 3)*(remain4 >= 2)*remain4, 'start_height': 0.3 + h1 + h2 + h3,
              "end_height": 0.3 + h1 + h2 + h3 + h4}

  # Sixth product : Paper pulp
  d5 = h7 - (0.3 + h1 + h2 + h3 + h4)
  quot5, remain5 = divmod(d5, 4.8)
  if remain5 >= 2.4:
      h5 = quot5*4.8 + remain5
  else:
      h5 = quot5*4.8
  paper = {"product": "paper", 'number': quot5 + (remain5 >= 2.4)*1, "length": h5, 'option1': 4.8,
            'option2': (remain5 >= 2.4)*remain5, 'start_height': 0.3 + h1 + h2 + h3 + h4,
            "end_height": 0.3 + h1 + h2 + h3 + h4 + h5}

  # Seventh product : Firewood
  d6 = h7 - (0.3 + h1 + h2 + h3 + h4 + h5)
  quot6, remain6 = divmod(d6, 1)
  if remain6 >= 0.5:
      h6 = quot6 * 1 + remain6
  else:
      h6 = quot6 * 1
  fire = {"product": "fire", 'number': quot6 + (remain6 >= 0.5) * 1, "length": h6, 'option1': 1,
          'option2': (remain6 >= 0.5) * remain6, 'start_height': 0.3 + h1 + h2 + h3 + h4 + h5,
          "end_height": 0.3 + h1 + h2 + h3 + h4 + h5 + h6}

  # Eight product: Toplog
  toplog = {"product": "toplog", 'number' : 1, 'length': ht - (0.3 + h1 + h2 + h3 + h4 + h5 + h6), "option1": "",
            "option2": "", 'start_height': 0.3 + h1 + h2 + h3 + h4 + h5 + h6,
            "end_height": ht}

  dico = [stump, furniture, lumber, sawing, particle, paper, fire, toplog]
  df = pd.DataFrame.from_dict(dico)
  df = df[df['number'] > 0]
  df['volume'] = df.apply(lambda row: volume_calculator(row['start_height'], row['end_height'],dbh, ht, a1, a2, b1, b2, b3, b4), axis = 1)

  return df