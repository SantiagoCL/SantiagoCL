import pickle
import os
import sectionproperties.pre.sections as sections
from sectionproperties.analysis.cross_section import CrossSection

class c_w_lps_profile():
    '''Perfil C con labios de refuerzos.

    # Parametros
    H: altura
    B: ancho
    D: largo del labio
    t: espesor
    r_out: Radio externo de los plegados
    name: Nombre para el perfil, sino se asigna uno por defecto
    plot: Grafica el perfil, centro de corte y centroide
    load: Cargar desde un archivo la seccion. Solo si name=''

    # Tests
    >>> p1 = c_w_lps_profile(H = 100, B = 50, D = 12, t = 1.5, r_out = 3.75)
    >>> round( p1.A, 2)
    319.04
    >>> round( p1.rx, 2)
    40.27
    >>> round( p1.c_x, 2)
    16.33
    '''

    def __init__(self, H, B, D, t, r_out, name = '', plot = False, load = 'True'):
        self.B = B
        self.D = D
        self.H = H
        self.t = t
        self.r_out= r_out
        
        defName = 'Cee_H'+str(H)+str(D)+'_B'+str(B)+'_t'+str(t)+'_r-out'+str(r_out)
        # creo un nombre para la seccion
        if not name:
            self.name = defName

        ## CALCULO PROPIEDADES A PARTIR DEL PAQUETE sectionproperties
        geometry = sections.CeeSection(d=H, b=B, l=D, t=t, r_out=r_out, n_r=8)
        # create mesh
        mesh = geometry.create_mesh(mesh_sizes=[t/4.0])
        # creo la seccion
        section = CrossSection(geometry, mesh)
        # calculo las propiedades
        section.calculate_geometric_properties()
        section.calculate_warping_properties()

        if plot:
            section.plot_centroids()

        (c_x, c_y) = section.get_c() # centroides
        (sc_x, sc_y) = section.get_sc() # shear center
        Cw = section.get_gamma() # warping
        (rx, ry) = section.get_rc()
        J = section.get_j()
        A = section.get_area()
        
        self.rx = rx
        self.ry = ry
        self.c_x = c_x
        self.sc_x = sc_x
        self.A = A
        self.Cw = Cw
        self.J = J

    def effective(self):
        raise NotImplementedError



def saveItem(item, fileName, mode = 'o'):
    '''Guarda en un archivo binario de nombre file la variable item.

    Por default hace un chequeo de existencia del archivo y solicita la confirmacion de sobreescritura.
    Si se desea sobreescribir directamenete, incluir una tercera variable con el caracter 'o'

    Requiere importar el paquete pickle

    Ejemplos:

    -------------------------------------------
    import pickle

    a = ['a','b', 'c']
    saveItem(a, 'aList.f')

    La variable -a- se puede recuperar con:
    file = open("aList.f", "rb")
    a = pickle.load(file)
    file.close()

    -------------------------------------------

    #Los items se pueden cargar con:
    file = open("item_0.dict", "rb")
    item = pickle.load(file)
    -------------------------------------------

    '''
    # modo de confirmacion para reemplazar archivos
    if mode == 'r':            
        nFile = fileName
        while os.path.isfile(nFile):
            print('File ' + nFile + ' already exist. Enter a new name or press Enter to replace.')
            nFile = input('')
            # En caso de que se quiera reemplazar otro archivo, guardo el nuevo nombre:
            if nFile: fileName = fileName
        if nFile: fileName = nFile

    with open(fileName, "wb") as file:
        pickle.dump(item, file)
