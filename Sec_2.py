'''Ecuaciones de la seccion 2 de ASCE - 8 - 02

'''

from math import pi
import numpy as np

class  sec2_1_1():
    '''Section 2.1.1: Dimensional Limits and Considerations.

    # Parametros
    profile: Dimensiones del perfil
    stiffCondition: Rigidización de los elementos 'UNSTIFFNED' (iii) | STIFFNED_SL (i) | STIFFNED (ii)

    '''
    #valores predefinidos
    def __init__(self, member, stiffCondition = 'UNSTIFFNED'):
        self.Name = 'Sec2.1.1'
        self.w = member.profile.w
        self.wf = member.profile.w
        self.t = member.profile.t
        self.L = member.L
        self.stiffCondition = stiffCondition

    def Cl_1(self):
        ''' Determina la relación máxima entre el ancho del ala y su esperor. Los valores limites se dan para tres condiciones de rigidización
        '''
        if self.stiffCondition == 'UNSTIFFNED':
            ratioAdm = 50.0 # 2.1.1-1.iii
            ratio = self.w/self.t
            print ('Esbeltez =',ratio, '<','Esbeltez admisible =', ratioAdm)
            return ratio < ratioAdm
        elif self.stiffCondition == 'STIFFNED':
            ratioAdm = 400.0 # 2.1.1-1.ii
            ratio = self.w/self.t
            print (ratio, '<', ratioAdm)
            return ratio < ratioAdm
        elif self.stiffCondition == 'STIFFNED_SL':
            ratioAdm = 90.0 # 2.1.1-1.ii
            ratio = self.w/self.t
            print (ratio, '<', ratioAdm)
            return ratio < ratioAdm
    def Cl_2(self):
        raise 'Not implemented'
    def Cl_3(self):
        '''Especifica el ancho efectivo en el caso de vigas cortas soportando una carga puntual.
        '''
        if self.L < 30*self.wf:
            self.ratio = self.TABLE1()
        else:
            self.ratio = 1.0
        self.w_eff = self.w*self.ratio
    def TABLE1(self):
        '''TABLE 1. Short, Wide Flanges: Maximum Allowable Ratio of Effective Design Width to Actual Width

        # Tests

        >>> TABLE1()
        '''
        table1 = np.array(((30, 1.00),
                (25, 0.96),
                (20, 0.91),
                (18, 0.89),
                (16, 0.86),
                (14, 0.82),
                (12, 0.78),
                (10, 0.73),
                (8, 0.67),
                (6, 0.55),
        ))
        r = np.interp( table1[:,0], table1[:,1], self.L/self.wf )
        return r
########################### USO
'''#INPUT:
flangeCURLING = 'False'
shearLag = 'True'
# VERIFICACION
for member in members:
    sec2_1_1 = sec2_1_1(memberProperties(member))
    print ('Los elementos del miembro', member, 'cumplen con las dimensiones requeridas:', sec2_1_1.Cl_1())
    if flangeCURLING:
        sec2_1_1.Cl_2
    if shearLag:
        sec2_1_1.Cl_3'''

def E_5_5_1(E0,K,L):
    '''Calcula la carga critica de euler para el caso stiffned

    # Tests
    >>> round( E_5_5_1(186200, 1.5, 200) ,2)
    20.42

    '''
    Pcr = pi**2* E0 / (K*L)**2
    return Pcr

def E_5_5_2(E0,K,L):
    '''Calcula la carga critica de euler para el caso unstiffned

    # Parametros
    E0: Modulo elasticidad incial
    K: Factor de longitud efectiva
    L: Longitud del miembro

    # Tests
    >>> round( E_5_5_2(E0 = 186200, K = 1.5, L = 200) ,2)
    10.21

    '''
    Pcr = pi**2* E0 / (K*L)**2*0.5
    return Pcr

def E_2_5(E0, K, L):
    '''Carga de pandeo lateral-torsional.

    # Parametros

    # Tests
    >>> round( E_2_5(E0 = 186200, K = 1.5, L = 200) ,2)
    20.42

    '''
    LTB = pi**2* E0 / (K*L)**2
    return LTB
