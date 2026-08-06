from ansys.stk.core.stkobjects import (
    STKObjectType,
    PropagatorType,
    SensorPattern,
)

def makeSatellite(scenario, satellite_name, propagator_type=PropagatorType.SGP4):
    """
    Creates a satellite in the given scenario with the specified name and sets its propagator type to SGP4 by default.

    Inputs:
    - scenario: The STK scenario object where the satellite will be created.
    - satellite_name: The name of the satellite to be created.
    - propagator_type: The type of propagator to be used for the satellite (default

    Output:
    - satellite: The created satellite object.
    """

    # Add the satellite to the scenario
    satellite = scenario.children.new(STKObjectType.SATELLITE, satellite_name)
    satellite.set_propagator_type(propagator_type)

    return satellite

def makeFacility(scenario, facility_name, position):
    """
    Creates a facility in the given scenario with the specified name.

    Inputs:
    - scenario: The STK scenario object where the facility will be created.
    - facility_name: The name of the facility to be created.
    - position: (Latitude, Longitude, Altitude) tuple representing the facility's position in degrees and meters.
    
    Outputs:
    - facility: The created facility object.
    """

    # Add the facility to the scenario
    facility = scenario.children.new(STKObjectType.FACILITY, facility_name)
    facility.position.assign_planetodetic(*position)

    return facility

def makeSensor(facility, sensor_name, sensor_parent, sensor_pattern):
    """
    Creates a sensor under the given parent object (facility or satellite) with the specified name and pattern.

    Inputs:
    - facility: The STK facility object where the sensor will be created.
    - sensor_name: The name of the sensor to be created.
    - sensor_parent: The parent object (facility or satellite) under which the sensor will be created.

    Outputs:
    - sensor: The created sensor object.
    """

    # Add the sensor to the parent object
    sensor = sensor_parent.children.new(STKObjectType.SENSOR, sensor_name)
    sensor.set_pattern_type(sensor_pattern)

    return sensor