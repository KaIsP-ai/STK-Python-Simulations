# Ansys Libraries
from ansys.stk.core.stkdesktop import STKDesktop
from ansys.stk.core.stkengine import STKEngine
from ansys.stk.core.stkobjects import (
    STKObjectType,
    SensorPattern,
    AccessConstraintType,
    ConstraintLighting,
    DataProviderGroup,
    VehicleAttitude,
    AttitudeProfile,
    PropagatorType
)

# Other Libraries
import sys
from pathlib import Path
import csv
import time

# Ensure the scripts see all directories in the environment
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Internal Libraries
from HelperFunctions.ScenarioCreation import (
    makeSatellite,
    makeFacility,
    makeSensor
)

from HelperFunctions.HPOP_ForceModel_Settings import (
    DragSettings,
    CentralBodyGravitySettings,
    ThirdBodyGravitySettings,
    SolarRadiationPressureSettings,
    GeneralSettings
)

# STKEngine Settings
USE_ENGINE = False
USE_ENGINE_GRAPHICS = False

# STKDesktop Settings
USER_CONTROL = True

# Save Settings
SAVE_SCENARIO = False
CLOSE_SCENARIO = False

# Scenario Settings
ANGLES_UNITS_PREFERENCE = "deg" # deg or rad

# Choose whether to open an engine or desktop instance
if USE_ENGINE:
    stk = STKEngine.start_application(no_graphics=not USE_ENGINE_GRAPHICS)
    root = stk.new_object_root()
    print(f"STKEngine instance started. Using version {stk.version}")
else:
    stk = STKDesktop.start_application(visible=True, user_control=USER_CONTROL)
    root = stk.root
    print("STKDesktop instance started")

# Creating a scenario
scenario_name = "HPOP_Sim"
root.new_scenario(scenario_name)
scenario = root.current_scenario

scenario.set_time_period("5 Jun 2022", "6 Jun 2022")
root.rewind()

root.units_preferences.item("LatitudeUnit").set_current_unit(ANGLES_UNITS_PREFERENCE)
root.units_preferences.item("LongitudeUnit").set_current_unit(ANGLES_UNITS_PREFERENCE)

print(f"Scenario '{scenario_name}' created with time period {scenario.start_time} to {scenario.stop_time}")

"""
-------------------------------------
        START MAIN CODE BLOCK
-------------------------------------
"""

# Adding objects to the scenario
print("Generating satellite with HPOP propagator")
satellite_name = "Eora_1"
satellite = makeSatellite(scenario, satellite_name)

satellite.set_attitude_type(VehicleAttitude.STANDARD)
basic = satellite.attitude.basic
basic.set_profile_type(AttitudeProfile.CENTRAL_BODY_FIXED)

satellite.set_propagator_type(PropagatorType.HPOP)
propagator = satellite.propagator
"""
Can set a range of parameters for the HPOP propagator:
- Covariance Matrix
- Ephemeric Interval
- Force Model
    - Central Body Gravity
        - Degree and Order
        - Gravity Model File
        - Solid Tides
        - Ocean Tides
        - Secular Variations
    - Third Body Gravity
    - Drag
        - Drag model/Drag model type
        - Solar/Geomagnetic Flux
        - Atmospheric density model
        - Blending range (low altitude)
    - Eclipsing Bodies
    - Solar Radiation Pressure
        - Shadow model
        - SRP Model
        - Boundary mitigation
    - More Options
        - Approx. Altitude
        - True vs. Actual Sun pos.
        - Ocean Tides settings
        - Solid tide settings
        - Extra radiation settings x2
        - Satellite mass
        - Relativistic acceleration
        - External Plugins (maybe tether)
- Initial State
    - Representation
    - Epoch
- Integrator
    - ???
- Step Size
"""
CentralBodyGravitySettings(propagator.force_model, 70, 70)

ThirdBodyGravitySettings(propagator.force_model.third_body_gravity, [], [])

# Currently not updating solar flux and atmospheric density model
DragSettings(propagator.force_model.drag, Cd=2.2, Area_Mass_Ratio=0.01)

print("Starting propagation")
start_time = time.perf_counter()
propagator.propagate()
end_time = time.perf_counter()
elapsed = end_time - start_time
print(f"Successfully propagated. Simulation took {elapsed} seconds")

"""
-------------------------------------
        END MAIN CODE BLOCK
-------------------------------------
"""

if SAVE_SCENARIO:
    # Make directory to save to
    directory = Path.cwd() / "Scenarios" / scenario_name
    directory.mkdir(parents=True, exist_ok=True)

    # Save the scenario to the directory
    path = directory / f"{scenario_name}.sc"
    root.save_as(str(path))
    if CLOSE_SCENARIO:
        root.close_scenario()

    print(f"Scenario saved to {path}")

# Shutdown the STK Engine instance if it was used
if USE_ENGINE:
    stk.shutdown()