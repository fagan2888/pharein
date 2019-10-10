


from . import globals

class UniformModel(object):

    def __init__(self, b=(1., 0., 0.), e=(0., 0., 0.), **kwargs):

        self.model = {"model": "model", "model_name": "uniform"}

        if globals.sim is None:
            raise RuntimeError("A simulation must be declared before a model")

        if globals.sim.model is not None:
            raise RuntimeError("A model is already created")

        else:
            globals.sim.set_model(self)

        if len(b) != 3 or (not isinstance(b, tuple) and not isinstance(b, list)):
            raise ValueError("invalid B")
        if len(e) != 3 or (not isinstance(e, tuple) and not isinstance(e, list)):
            raise ValueError("invalid E")


        self.model.update({"bx": lambda x : b[0],
                           "by": lambda x :  b[1],
                           "bz": lambda x : b[2],
                           "ex": lambda x : e[0],
                           "ey": lambda x : e[1],
                           "ez": lambda x : e[2]})


        self.populations = kwargs.keys()
        for population in self.populations:
            self.add_population(population, **kwargs[population])




# ------------------------------------------------------------------------------

    def nbr_populations(self):
        """
        returns the number of species currently registered in the model
        """
        keys = self.model.keys()
        nbr = 0
        for k in keys:
            if k.startswith('population'):
                nbr += 1
        return nbr

#------------------------------------------------------------------------------

    def add_population(self, name,
                        charge=1,
                        mass=1,
                        nbr_part_per_cell=100,
                        density=1.,
                        vbulk=(0., 0., 0.),
                        beta=1.0,
                        anisotropy=1.):
        """
        add a particle population to the current model

        add_population(name,charge=1, mass=1, nbrPartCell=100, density=1, vbulk=(0,0,0), beta=1, anisotropy=1)

        Parameters:
        -----------
        name        : name of the species, str

        Optional Parameters:
        -------------------
        charge      : charge of the species particles, float (default = 1.)
        nbrPartCell : number of particles per cell, int (default = 100)
        density     : particle density, float (default = 1.)
        vbulk       : bulk velocity, tuple of size 3  (default = (0,0,0))
        beta        : beta of the species, float (default = 1)
        anisotropy  : Pperp/Ppara of the species, float (default = 1)
        """

        idx = str(self.nbr_populations())

        new_population = {name: {
                          "charge": charge,
                          "mass": mass,
                          "density": lambda x : density,
                          "vx": lambda x : vbulk[0],
                          "vy": lambda x : vbulk[1],
                          "vz": lambda x : vbulk[2],
                          "beta": lambda x : beta,
                          "anisotropy": lambda x : anisotropy,
                          "nbrParticlesPerCell": lambda x : nbr_part_per_cell}}

        keys = self.model.keys()
        if name in keys:
            raise ValueError("population already registered")

        self.model.update(new_population)
#------------------------------------------------------------------------------

    def to_dict(self):
        self.model['nbr_ion_populations'] = self.nbr_populations()
        return self.model
