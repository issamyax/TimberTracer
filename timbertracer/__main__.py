#Internal imports
import app
import config as ttdata

if __name__ == '__main__':

    sim_jardin_BAU = app.run_model(
        scale = 20.33, shape= 5.65, class_width = 1 , tolerance_g = 0.3,
        a1 = 0.6626, a2 = 0.8769, b1= 0.9712, b2 = -0.2774, b3 = 1.1107,
        b4 = 26.4390, a = 0.7, c = 1, alpha = 0.04, beta = 2.10,
        tolerance_hfind = 0.0001, efficiency = ttdata.efficiency, 
        loss_allocation = ttdata.loss_allocation, recycling = ttdata.recycling_BAU,
        substitution_matrix = ttdata.substitution_matrix, 
        decay = ttdata.decay, PH = 141, R = 0, management_dic = ttdata.management_jardin)