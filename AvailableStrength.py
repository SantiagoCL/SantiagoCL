'''Modulo de diseño de estructuras metalicas segun ASCE - 8

    #Tests

    ## steel
    >>> mat = steel(344.8,186200.0, 0.3, 4.58, 0.002, name = 'SA304_1_4Hard')
    >>> round(mat.Et(159.3),2)
    141952.2
    >>> round(mat.Es(159.3),2)
    174334.98
    >>> round(mat.eta(159.3),4)
    0.7624
    >>> mat.name
    'SA304_1_4Hard'
    
    ## member
    >>> m = member(100, 'Uno')
    Advertencia: El miembro Uno no tiene asignado ningun pefil.
    Advertencia: El miembro Uno no tiene asignado ningun acero.
    Advertencia: El miembro Uno no tiene asignado parametros de diseño.

    ## ASCE_8_02
    >>> p = c_w_lps_profile(10,2,50)
    >>> s = steel(344,186200)
    >>> dP = designParameters(1.5,'unstiffned')
    >>> m = member(200,'2', p, s, dP)
    >>> analysis = ASCE_8_02(m)
    >>> round( analysis.Cl_5_5(), 2)
    10.21
    >>> analysis.member.dP.stiffCondition = 'stiffned'
    >>> round( analysis.Cl_5_5(), 2)
    20.42
    >>> round( analysis.Cl_2_5(), 2)
    20.42

    ## sec2_1_1 aplicado a un perfil C
    >>> v_sec2_1_1 = sec2_1_1(m)
    >>> v_sec2_1_1.Cl_1()
    Esbeltez = 5.0 < Esbeltez admisible = 50.0
    True
    >>> 

'''

from math import pi
from Sec_2 import E_5_5_1, E_5_5_2, E_2_5, sec2_1_1
from Sec_3 import E3_4_3_e1
from Appendix_B import B_2, B_1
from profiles import c_w_lps_profile

class steel():
    ''' Creo un acero. 

        Métodos:

        Et(s) = Módulo elastico tangente a la tensión s
        Es(s) = Módulo elastico secante a la tensión s
        eta(s) = Factor de plasticidad a la tensión s

    '''

    def __init__(self, FY, E0, nu = 0.3, n = 1.0, offset = 0.0, name = ''):
        self.FY = FY
        self.nu = nu
        self.n = n
        self.offset = offset
        self.E0 = E0
        self.name = name

    def Et(self, s):
        ''' Modulo elastico tangente. Eq B-2

        
        '''
        Et = B_2(self.FY, self.E0, self.offset, self.n, s)
        return Et
    
    def Es(self, s):
        ''' Modulo elastico secante. Eq B-1

        '''
        Es = B_1(self.FY, self.E0, self.offset, self.n, s)
        return Es

    def eta(self, s):
        ''' Factor de plasticidad. Et/E0 Eq B-5

        '''
        return self.Et(s) / self.E0




class designParameters:
    '''Parametro de diseño asociados a un miembro.

    # Parametros
    K = Factor de longitud efectiva
    stiffCondition = Rigidización de los elementos 'UNSTIFFNED' (iii) | STIFFNED_SL (i) | STIFFNED (ii)

    '''
    def __init__(self, K, stiffCondition):
        self.K = K
        self.stiffCondition = stiffCondition

class member():
    ''' Crea un miembro estructural.

    # Parametros
    L:                  Longitud
    profile:            Clase profile con dimensiones y metodos de la seccion estructural 
    steel:              Clase steel con las propiedades mecanicas y metodos
    designParameters:   Clase con los parametros de diseño a considerar en el miembro

    '''

    def __init__(self, L, name = 'none', profile = '', steel = '', designParameters = ''):

        self.name = name
        self.L = L
        if not profile:
            print ('Advertencia: El miembro', self.name, 'no tiene asignado ningun pefil.')
        else:
            self.profile = profile

        if not steel:
            print ('Advertencia: El miembro', self.name, 'no tiene asignado ningun acero.')
        else:
            self.steel = steel

        if not designParameters:
            print ('Advertencia: El miembro', self.name, 'no tiene asignado parametros de diseño.')
        else:
            self.dP = designParameters

class ASCE_8_02:
    ''' Verificaciones segun ASCE 8 / Sec. 5

    # Parametros
    member
    
    '''

    def __init__(self, member):
        self.member = member
        if not member.profile:
            print ('Advertencia: El miembro', member.name, 'no tiene asignado ningun pefil.')
        if not member.steel:
            print ('Advertencia: El miembro', member.name, 'no tiene asignado ningun acero.')
        if not designParameters:
            print ('Advertencia: El miembro', member.name, 'no tiene asignado parametros de diseño.')

    def Cl_5_5(self):
        '''Carga critica de Euler

        ASCE_8_02.Eq_5_5_i.__doc__
        '''
        E0 = self.member.steel.E0
        L = self.member.L
        K = self.member.dP.K

        if self.member.dP.stiffCondition == 'stiffned':
            Pcr = E_5_5_1(E0, K, L)
        elif self.member.dP.stiffCondition == 'unstiffned':
            Pcr = E_5_5_2(E0, K, L)
        return Pcr

    def Cl_2_5(self):
        
        E0 = self.member.steel.E0
        L = self.member.L
        K = self.member.dP.K

        LTB = E_2_5(E0, K, L)
        return LTB


'''
steel(344.8,186200.0, 0.3, 4.58, 0.002, name = 'SA304_1_4Hard').eta(159.3)

members = []
p = C_profile(4,2,50)
s = steel(344,186200)
dP = designParameters(1.5,'stiffned')
m = member(100,'1', p, s, dP)
members.append(m)
p = C_profile(4,2,50)
s = steel(344,186200)
dP = designParameters(1.5,'unstiffned')
m = member(200,'2', p, s, dP)
members.append(m)


for member in members:
    analysis = ASCE_8_02(member)
    print ('Miembro:',member.name,'| Ala:', member.dP.tipoAla, '| Pcr:',round(analysis.Cl_5_5(),2))
    print ('Miembro:',member.name,'| LTB:',round(analysis.Cl_2_5(),2))
    '''

def Fn(L, eta):
    Fn = E3_4_3_e1(E0 = 180510, Kx = 0.5, Lx = L, Kt = 0.5, Lt = L, rx = 40.272, ry = 18.2673,
                    eta = eta, c_x = 15.59, sc_x = 23.1, A = 319, Cw = 215e6, G0 = 69426.9, J = 239)
    return Fn

def F_FTB(L, s = 0):
    '''

    #Test
    >>> round( F_FTB(100), 2)
    430.27
    >>> round( F_FTB(1000), 2)
    300.5
    >>> round( F_FTB(2000), 2)
    251.03
    >>> round( F_FTB(3000), 2)
    159.59

    '''
    mat = steel(FY= 337, E0 = 180510, nu = 0.3, n = 13.5, offset = 0.002)
    
    # tension inicial para iterar
    if not s:
        s = mat.FY*0.75
    ds = 0.1
    # error tolerado porcentual
    err = 1
    #inicializo el contador de iteraciones
    iterr = 0
    #inicializo eta
    eta = mat.eta(s)
    #calculo el primer valor de Fn para eta = 1
    FF =Fn(L, 1)
    F = FF*eta

    # funcion para encontrar raices
    fn = s - F
    
    # newton-rapson para encontrar raiz de fn
    while abs((F-s)/s*100) > err and iterr < 100:
        eta_2 = mat.eta(s+ds)
        F_2 = FF*eta_2
        fn_2 = s+ds - F_2
        dfn = (fn_2 - fn)/ds
        s = s - fn/dfn

        eta = mat.eta(s)
        F = FF*eta
        fn = s - F
        iterr += 1
        #print(iterr, s, F, 100-(F-s)/s*100)
    if abs((F-s)/s*100) > err:
        print('Se excedieron las 100 iteraciones')
    return F

for L in range(100,4000,100):
    print(F_FTB(L)*319)
