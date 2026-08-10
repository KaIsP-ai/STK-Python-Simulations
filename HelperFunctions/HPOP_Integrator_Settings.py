from ansys.stk.core.stkobjects import (
    VehicleIntegrationMethod,
    VehicleInterpolationMethod,
)

"""
-------------------------
GeneralIntegratorSettings
-------------------------
Updates certain general settings of the HPOP propagator.

INPUTS:

- integrator = The HPOP integrator object to modify.

Optional:
- Allow_Position_Velocity_Covariance_Interpolation = Boolean describing whether position and velocity covariance interpolation is allowed. (I don't see a way to set this to false)
- Do_Not_Propagate_Below_Altitude = Altitude below which the propagator will not propagate.
- Report_Ephemeris_Fixed = Boolean describing whether the ephemeris should be reported in a fixed time step. Sets Time Regularisation to False.
"""

def GeneralIntegratorSettings(
    integrator,

    Allow_Position_Velocity_Covariance_Interpolation=None,
    Do_Not_Propagate_Below_Altitude=None,
    Report_Ephemeris_Fixed=None
):
    print("Updating General Integrator Settings")

    if Allow_Position_Velocity_Covariance_Interpolation is not None:
        integrator.allow_position_velocity_covariance_interpolation = Allow_Position_Velocity_Covariance_Interpolation
        print(f"- Allowed Position Velocity Covariance Interpolation set to {Allow_Position_Velocity_Covariance_Interpolation}")
    else:
        print(f"- No allow position velocity covariance interpolation setting provided. Using default value")
    
    if Do_Not_Propagate_Below_Altitude is not None:
        integrator.do_not_propagate_below_altitude = Do_Not_Propagate_Below_Altitude
        print(f"- Do Not Propagate Below Altitude set to {Do_Not_Propagate_Below_Altitude}")
    else:
        print(f"- No do not propagate below altitude setting provided. Using default value")

    if Report_Ephemeris_Fixed is not None:
        integrator.time_regularisation.use_regularised_time = False
        integrator.report_ephemeris_on_fixed_time_step = Report_Ephemeris_Fixed
        print(f"- Report Ephemeris Fixed set to {Report_Ephemeris_Fixed} and Time Regularisation set to False")
    else:
        print(f"- No report ephemeris fixed setting provided. Using default value")

    print("Finished updating General Integrator Settings")





"""
---------------------
InterpolationSettings
---------------------
Updates certain interpolation settings of the HPOP propagator.

INPUTS:

- integrator = The HPOP integrator object to modify.
- Interpolation_Method = Interpolation method to use. (Enum=VehicleInterpolationMethod)

Optional:
- Interpolation_Order = Order of interpolation.
- Gravitational_Parameter = Gravitational parameter to use. Type=VOP
"""

def InterpolationSettings(
    integrator,

    Interpolation_Method,
    Interpolation_Order=None,

    Gravitational_Parameter=None
):
    print("Updating interpolation settings")

    integrator.interpolation.method = Interpolation_Method
    print(f"- Interpolation Method set to {Interpolation_Method}")

    if Interpolation_Order is not None:
        integrator.interpolation.order = Interpolation_Order
        print(f"- Interpolation Order set to {Interpolation_Order}")
    else:
        print(f"- No interpolation order provided. Using default value")

    if Interpolation_Method == VehicleInterpolationMethod.VOP:
        if Gravitational_Parameter is not None:
            integrator.interpolation.vop_mu = Gravitational_Parameter
            print(f"- Gravitational Parameter set to {Gravitational_Parameter}")
        else:
            print(f"- No gravitational parameter provided. Using default value")
    else:
        print(f"- Gravitational parameter not applicable for interpolation method {Interpolation_Method}")

    print("Finished updating interpolation settings")





"""
----------------
StepSizeSettings
----------------
Updates certain step size settings of the HPOP propagator.

INPUTS:

- integrator = The HPOP integrator object to modify.
- StepSize_Method = Step size method to use. (Enum=VehicleMethod)

Optional:
- Max_StepSize = Maximum step size to use. Type=RELATIVE_ERROR
- Min_StepSize = Minimum step size to use. Type=RELATIVE_ERROR
- Error_Tolerance = Error Tolerance allowed. Type=RELATIVE_ERROR
"""

def StepSizeSettings(
    integrator,

    StepSize_Method,

    Max_StepSize=None,
    Min_StepSize=None,
    Error_Tolerance=None
):
    print("Updating step size settings")

    integrator.step_size_control.method = StepSize_Method
    print(f"- Step Size Method set to {StepSize_Method}")

    if Max_StepSize is not None:
        integrator.step_size.max_step_size = Max_StepSize
        print(f"- Max Step Size set to {Max_StepSize}")
    else:
        print(f"- No max step size provided. Using default value")

    if Min_StepSize is not None:
        integrator.step_size.min_step_size = Min_StepSize
        print(f"- Min Step Size set to {Min_StepSize}")
    else:
        print(f"- No min step size provided. Using default value")

    if StepSize_Method == VehicleIntegrationMethod.RELATIVE_ERROR:
        if Error_Tolerance is not None:
            integrator.step_size.relative_error_tolerance = Error_Tolerance
            print(f"- Error Tolerance set to {Error_Tolerance}")
        else:
            print(f"- No error tolerance provided. Using default value")
    else:
        print(f"- Error tolerance not applicable for step size method {StepSize_Method}")

    print("Finished updating step size settings")





"""
-----------------------
RegularisedTimeSettings
-----------------------
Regularised time settings for the HPOP propagator.

INPUTS:

- integrator = The HPOP integrator object to modify.
- Use_Regularised_Time = Boolean describing whether to use regularised time. Sets Report Ephemeris Fixed to False.

Optional:
- Exponent = Exponent to use for regularised time.
- Steps_Per_Orbit = Number of steps per orbit to use for regularised time.
"""

def RegularisedTimeSettings(
    integrator,

    Use_Regularised_Time,

    Exponent=None,
    Steps_Per_Orbit=None
):
    print("Updating regularised time settings")

    integrator.report_ephemeris_on_fixed_time_step = False
    print(f"- Report Ephemeris Fixed set to False")
    integrator.regularised_time.use_regularised_time = Use_Regularised_Time
    print(f"- Use Regularised Time set to {Use_Regularised_Time}")

    if Use_Regularised_Time:
        if Exponent is not None:
            integrator.regularised_time.exponent = Exponent
            print(f"- Exponent set to {Exponent}")
        else:
            print(f"- No exponent provided. Using default value")

        if Steps_Per_Orbit is not None:
            integrator.regularised_time.steps_per_orbit = Steps_Per_Orbit
            print(f"- Steps Per Orbit set to {Steps_Per_Orbit}")
        else:
            print(f"- No steps per orbit provided. Using default value")

    print("Finished updating regularised time settings")





"""
------------------
setBulirschStoer
------------------
Sets the HPOP integrator to use the Bulirsch-Stoer method.
Applies any settings changes specific to this integrator.

INPUTS:

- integrator = The HPOP integrator object to modify.

Optional:
- Use_VOP_UniversalVariables = Boolean describing whether to use VOP universal variables. Mandates use of VOP Interpolation Method.

INPUTS for Step Size Settings:
- StepSize_Method = Step size method to use. (Enum=VehicleMethod)

Optional:
- Max_StepSize = Maximum step size to use. Type=RELATIVE_ERROR
- Min_StepSize = Minimum step size to use. Type=RELATIVE_ERROR
- Error_Tolerance = Error Tolerance allowed. Type=RELATIVE_ERROR

INPUTS for Interpolation Settings (automatically uses VOP if Use_VOP_UniversalVariables is True):
- Interpolation_Method = Interpolation method to use. (Enum=VehicleInterpolationMethod)

Optional:
- Interpolation_Order = Order of interpolation.
- Gravitational_Parameter = Gravitational parameter to use. Type=VOP
""" 

def setBulirschStoer(
    integrator,

    StepSize_Method,
    Interpolation_Method,

    Use_VOP_UniversalVariables=None,

    Max_StepSize=None,
    Min_StepSize=None,
    Error_Tolerance=None,

    Interpolation_Order=None,
    Gravitational_Parameter=None
):
    print("Setting integrator to Bulirsch-Stoer")

    integrator.integration_model = VehicleIntegrationMethod.BULIRSCH_STOER
    print(f"- Integrator method set to Bulirsch-Stoer")

    if Use_VOP_UniversalVariables is not None:
        integrator.use_graphics_3d_p = Use_VOP_UniversalVariables
        print(f"- Use VOP Universal Variables set to {Use_VOP_UniversalVariables}")
        if Use_VOP_UniversalVariables:
            Interpolation_Method = VehicleInterpolationMethod.VOP
            print(f"- Interpolation Method automatically set to VOP due to Use VOP Universal Variables being True")
    else:
        print(f"- No Use VOP Universal Variables setting provided. Using default value")

    StepSizeSettings(
        integrator=integrator,
        StepSize_Method=StepSize_Method,
        Max_StepSize=Max_StepSize,
        Min_StepSize=Min_StepSize,
        Error_Tolerance=Error_Tolerance
    )

    InterpolationSettings(
        integrator=integrator,
        Interpolation_Method=Interpolation_Method,
        Interpolation_Order=Interpolation_Order,
        Gravitational_Parameter=Gravitational_Parameter
    )

    print("Finished setting integrator to Bulirsch-Stoer")





"""
---------------
setGaussJackson
---------------
Sets the HPOP integrator to use the Gauss-Jackson method.
Applies any settings changes specific to this integrator.

INPUTS:

- integrator = The HPOP integrator object to modify.

Optional:
- Predictor_Corrector = Chooses the predictor corrector scheme (Enum=VehiclePredictorCorrectorScheme)

INPUTS for Interpolation Settings:
- Interpolation_Method = Interpolation method to use. (Enum=VehicleInterpolationMethod)

Optional:
- Interpolation_Order = Order of interpolation.
- Gravitational_Parameter = Gravitational parameter to use. Type=VOP
"""

def setGaussJackson(
    integrator,

    Interpolation_Method,

    Predictor_Corrector=None,

    Interpolation_Order=None,
    Gravitational_Parameter=None
):
    print("Setting integrator to Gauss-Jackson")

    integrator.integration_model = VehicleIntegrationMethod.GAUSS_JACKSON
    print(f"- Integrator method set to Gauss-Jackson")

    if Predictor_Corrector is not None:
        integrator.predictor_corrector_scheme = Predictor_Corrector
        print(f"- Predictor Corrector Scheme set to {Predictor_Corrector}")
    else:
        print(f"- No predictor corrector scheme provided. Using default value")

    InterpolationSettings(
        integrator=integrator,
        Interpolation_Method=Interpolation_Method,
        Interpolation_Order=Interpolation_Order,
        Gravitational_Parameter=Gravitational_Parameter
    )

    print("Finished setting integrator to Gauss-Jackson")





"""
--------------
setRungeKutta4
--------------
Sets the HPOP integrator to use the Runge-Kutta 4 method.
Applies any settings changes specific to this integrator.

INPUTS:
- integrator = The HPOP integrator object to modify.

Optional:
- Use_VOP_UniversalVariables = Boolean describing whether to use VOP universal variables. Mandates use of VOP Interpolation Method.

INPUTS for Interpolation Settings:
- Interpolation_Method = Interpolation method to use. (Enum=VehicleInterpolationMethod)

Optional:
- Interpolation_Order = Order of interpolation.
- Gravitational_Parameter = Gravitational parameter to use. Type=VOP
"""

def setRungeKutta4(
    integrator,

    Interpolation_Method,

    Use_VOP_UniversalVariables=None,

    Interpolation_Order=None,
    Gravitational_Parameter=None
):
    print("Setting integrator to Runge-Kutta 4")

    integrator.integration_model = VehicleIntegrationMethod.RUNGE_KUTTA_4
    print(f"- Integrator method set to Runge-Kutta 4")

    if Use_VOP_UniversalVariables is not None:
        integrator.use_graphics_3d_p = Use_VOP_UniversalVariables
        print(f"- Use VOP Universal Variables set to {Use_VOP_UniversalVariables}")
        if Use_VOP_UniversalVariables:
            Interpolation_Method = VehicleInterpolationMethod.VOP
            print(f"- Interpolation Method automatically set to VOP due to Use VOP Universal Variables being True")
    else:
        print(f"- No Use VOP Universal Variables setting provided. Using default value")

    InterpolationSettings(
        integrator=integrator,
        Interpolation_Method=Interpolation_Method,
        Interpolation_Order=Interpolation_Order,
        Gravitational_Parameter=Gravitational_Parameter
    )

    print("Finished setting integrator to Runge-Kutta 4")





"""
-----------------------
setRungeKuttaFehlberg78
-----------------------
Sets the HPOP integrator to use the Runge-Kutta-Fehlberg 7(8) method.
Applies any settings changes specific to this integrator.

INPUTS:

- integrator = The HPOP integrator object to modify.

Optional:
- Use_VOP_UniversalVariables = Boolean describing whether to use VOP universal variables. Mandates use of VOP Interpolation Method.

INPUTS for Step Size Settings:
- StepSize_Method = Step size method to use. (Enum=VehicleMethod)

Optional:
- Max_StepSize = Maximum step size to use. Type=RELATIVE_ERROR
- Min_StepSize = Minimum step size to use. Type=RELATIVE_ERROR
- Error_Tolerance = Error Tolerance allowed. Type=RELATIVE_ERROR

INPUTS for Interpolation Settings (automatically uses VOP if Use_VOP_UniversalVariables is True):
- Interpolation_Method = Interpolation method to use. (Enum=VehicleInterpolationMethod)

Optional:
- Interpolation_Order = Order of interpolation.
- Gravitational_Parameter = Gravitational parameter to use. Type=VOP
"""

def setRungeKuttaFehlberg78(
    integrator,

    StepSize_Method,
    Interpolation_Method,

    Use_VOP_UniversalVariables=None,

    Max_StepSize=None,
    Min_StepSize=None,
    Error_Tolerance=None,

    Interpolation_Order=None,
    Gravitational_Parameter=None
):
    print("Setting integrator to Runge-Kutta-Fehlberg 7(8)")

    integrator.integration_model = VehicleIntegrationMethod.RUNGE_KUTTA_FEHLBERG_78
    print(f"- Integrator method set to Runge-Kutta-Fehlberg 7(8)")

    if Use_VOP_UniversalVariables is not None:
        integrator.use_graphics_3d_p = Use_VOP_UniversalVariables
        print(f"- Use VOP Universal Variables set to {Use_VOP_UniversalVariables}")
        if Use_VOP_UniversalVariables:
            Interpolation_Method = VehicleInterpolationMethod.VOP
            print(f"- Interpolation Method automatically set to VOP due to Use VOP Universal Variables being True")
    else:
        print(f"- No Use VOP Universal Variables setting provided. Using default value")

    StepSizeSettings(
        integrator=integrator,
        StepSize_Method=StepSize_Method,
        Max_StepSize=Max_StepSize,
        Min_StepSize=Min_StepSize,
        Error_Tolerance=Error_Tolerance
    )

    InterpolationSettings(
        integrator=integrator,
        Interpolation_Method=Interpolation_Method,
        Interpolation_Order=Interpolation_Order,
        Gravitational_Parameter=Gravitational_Parameter
    )

    print("Finished setting integrator to Runge-Kutta-Fehlberg 7(8)")





"""
---------------------
setRungeKuttaVerner89
---------------------
Sets the HPOP integrator to use the Runge-Kutta-Verner 8(9) Efficient method.
Applies any settings changes specific to this integrator.

INPUTS:

- integrator = The HPOP integrator object to modify.

Optional:
- Use_VOP_UniversalVariables = Boolean describing whether to use VOP universal variables. Mandates use of VOP Interpolation Method.

INPUTS for Step Size Settings:
- StepSize_Method = Step size method to use. (Enum=VehicleMethod)

Optional:
- Max_StepSize = Maximum step size to use. Type=RELATIVE_ERROR
- Min_StepSize = Minimum step size to use. Type=RELATIVE_ERROR
- Error_Tolerance = Error Tolerance allowed. Type=RELATIVE_ERROR

INPUTS for Interpolation Settings (automatically uses VOP if Use_VOP_UniversalVariables is True):
- Interpolation_Method = Interpolation method to use. (Enum=VehicleInterpolationMethod)

Optional:
- Interpolation_Order = Order of interpolation.
- Gravitational_Parameter = Gravitational parameter to use. Type=VOP
"""

def setRungeKuttaVerner89(
    integrator,

    StepSize_Method,
    Interpolation_Method,

    Use_VOP_UniversalVariables=None,

    Max_StepSize=None,
    Min_StepSize=None,
    Error_Tolerance=None,

    Interpolation_Order=None,
    Gravitational_Parameter=None
):
    print("Setting integrator to Runge-Kutta-Verner 8(9) Efficient")

    integrator.integration_model = VehicleIntegrationMethod.RUNGE_KUTTA_VERNEr_89_EFFICIENT
    print(f"- Integrator method set to Runge-Kutta-Verner 8(9) Efficient")

    if Use_VOP_UniversalVariables is not None:
        integrator.use_graphics_3d_p = Use_VOP_UniversalVariables
        print(f"- Use VOP Universal Variables set to {Use_VOP_UniversalVariables}")
        if Use_VOP_UniversalVariables:
            Interpolation_Method = VehicleInterpolationMethod.VOP
            print(f"- Interpolation Method automatically set to VOP due to Use VOP Universal Variables being True")
    else:
        print(f"- No Use VOP Universal Variables setting provided. Using default value")

    StepSizeSettings(
        integrator=integrator,
        StepSize_Method=StepSize_Method,
        Max_StepSize=Max_StepSize,
        Min_StepSize=Min_StepSize,
        Error_Tolerance=Error_Tolerance
    )

    InterpolationSettings(
        integrator=integrator,
        Interpolation_Method=Interpolation_Method,
        Interpolation_Order=Interpolation_Order,
        Gravitational_Parameter=Gravitational_Parameter
    )

    print("Finished setting integrator to Runge-Kutta-Verner 8(9) Efficient")