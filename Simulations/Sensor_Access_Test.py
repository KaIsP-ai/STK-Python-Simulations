# Ansys Libraries
from ansys.stk.core.stkdesktop import STKDesktop
from ansys.stk.core.stkengine import STKEngine
from ansys.stk.core.stkobjects import (
    STKObjectType,
    SensorPattern,
    AccessConstraintType,
    ConstraintLighting,
    DataProviderGroup
)

# Other Libraries
import sys
from pathlib import Path
import csv

# Ensure the scripts see all directories in the environment
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Internal Libraries
from HelperFunctions.ScenarioCreation import (
    makeSatellite,
    makeFacility,
    makeSensor
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


"""
-------------------------------------
        START MAIN CODE BLOCK
-------------------------------------
"""

# Creating a scenario
scenario_name = "SatelliteAccessTest"
root.new_scenario(scenario_name)
scenario = root.current_scenario

scenario.set_time_period("5 Jun 2022", "6 Jun 2022")
root.rewind()

root.units_preferences.item("LatitudeUnit").set_current_unit(ANGLES_UNITS_PREFERENCE)
root.units_preferences.item("LongitudeUnit").set_current_unit(ANGLES_UNITS_PREFERENCE)

print(f"Scenario '{scenario_name}' created with time period {scenario.start_time} to {scenario.stop_time}")

# Adding objects to that scenario
satellite_name = "MySatellite"
satellite = makeSatellite(scenario, satellite_name)

facility_name = "MyFacility"
facility = makeFacility(scenario, facility_name, (-33.9176, 151.2318, 0))

sensor_name = "MySensor"
sensor_parent = facility
sensor = makeSensor(facility, sensor_name, sensor_parent, SensorPattern.SIMPLE_CONIC)
sensor.common_tasks.set_pattern_simple_conic(45, 1) # Sensor half angle, Angular resolution

# Calculate Access
access = facility.get_access_to_object(satellite)
access.compute_access()

access_intervals = access.computed_access_interval_times
print(access_intervals)

# Get data
for dp in satellite.data_providers:
    print(dp.name)

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