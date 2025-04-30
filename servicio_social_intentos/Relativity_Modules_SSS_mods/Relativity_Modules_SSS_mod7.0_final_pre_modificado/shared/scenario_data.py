import importlib


class Scenario:
    '''
    this must be defined as a class, since
    we'd like to create various instances
    of these objects depending on the chosen scenario.

    it gives us the minimum variables needed to
    define the differential equation.
    it makes things "modular"
    '''

    def __init__(self, r0, R0, mHS, rho, xrho, T, f, f1, f2, f3, f32):

        self.r0   = r0
        self.R0   = R0
        self.mHS  = mHS
        self.rho  = rho
        self.xrho = xrho
        self.T    = T
        self.f    = f
        self.f1   = f1
        self.f2   = f2
        self.f3   = f3
        self.f32  = f32

scenarios_map = {
    "Hu_Sawicki":    "scenarios.Hu_Sawicki.f_functions",  # R0: 12371.572599817798618 12371.572599817798618
    "alpha_L_L_M":   "scenarios.alpha_L_L_M.f_functions",  # R0 = 1.660731799228 1.660732198089454
    "lambda_L_L_M":  "scenarios.lambda_L_L_M.f_functions",  # R0 = 2.289814669280079 2.289814557737051
}

def load_scenario(name):
    '''
    defined to make the main file cleaner.

    :param name: the name of the scenario
    :return: the chosen scenario
    '''

    mod = importlib.import_module(scenarios_map[name])

    return Scenario(
          r0   = mod.r0,
          R0   = mod.R0,
          mHS  = mod.mHS,
          rho  = mod.rho,
          xrho = mod.xrho,
          T    = mod.T,
          f    = mod.f,
          f1   = mod.f1,
          f2   = mod.f2,
          f3   = mod.f3,
          f32  = mod.f32,
                        )
