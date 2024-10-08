

class COST_PARAMETERS:
    M : float = 200
    C_s : float = 0.27
    C_w : float = 200
    
class MACHINE_PARAMETERS:
    R_t : float = 0
    d_s : float = 250
    b_s : float = 25
    D_e : float = 350
    f : float = 0.3
    d : float = 0.1
    
class WORKPIECE_PARAMETERS:
    L_w : float = 250
    b_w : float = 30
    
class PROCESS_SETTINGS:
    Q_prime_l : float = 0.1
    Q_prime_u : float = 15
    Ra_max : 1.8
    burn_rough_threshold : 0.5
    burn_finish_threshold : 0.5
    a_total : 2.0
    

# Settings
# Constraint is True if feasible and false otherwise