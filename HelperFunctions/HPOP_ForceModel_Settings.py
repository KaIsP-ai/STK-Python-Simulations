"""
-------------
DragSettings:
-------------
Defines the drag settings for the HPOP simulation.
Handles setting changes on an input basis, such that certain settings are only changed if the user specifies a value for them.
For now we assume that the drag model being used is the default Spherical one, not a plugin so Cd and Mass_Area_Ratio are required inputs.

INPUTS:

- force_model = Container for the settings to be changed. Comes from propagator.force_model. Contains drag and more_options.
- Cd = Drag coefficient of the satellite.
- Area_Mass_Ratio = Mass to area ratio of the satellite.

Optional:
- Atm_Density_Model = The atmospheric density model to be used. If None, the default model will be used.
- SolarFlux_Model_Type = The solar flux model type to be used. If None, the default model will be used.
    - Comes from VehicleSolarFluxGeomagneticType
- SolarFlux_File = The solar flux model file to be used. Type=FILE
- SolarFlux_Update_Rate = The solar flux model update rate to be used. Type=FILE
- SolarFlux_Avg = The solar flux average rate to be used. Type=MANUAL_ENTRY
- SolarFlux_Daily = The solar flux daily rate to be used. Type=MANUAL_ENTRY
- Use_Apparent_Sun_Position = Boolean describing whether the apparent sun position should be used.
- Use_Approx_Altitude = Boolean describing whether the approximate altitude should be used.
"""

def DragSettings(
    force_model,
    Cd,
    Area_Mass_Ratio,

    Atm_Density_Model=None,

    SolarFlux_Model_Type=None,
    SolarFlux_File=None,
    SolarFlux_Update_Rate=None,
    SolarFlux_Avg=None,
    SolarFlux_Daily=None,

    Use_Apparent_Sun_Position=None,
    Use_Approx_Altitude=None,
):
    print("Updating drag settings")

    drag = force_model.drag
    more_options = force_model.more_options

    drag.use = True

    drag.drag_model.cd = Cd
    drag.drag_model.area_mass_ratio = Area_Mass_Ratio

    if Atm_Density_Model is not None:
        print("- Updating Atmospheric Density Model")
        # NEED TO DO
        print("- Haven't implemented functionality")
    else:
        print("- Using default Atmospheric Density Model")

    if SolarFlux_Model_Type is not None:
        print("- Updating Solar Flux Model Type")
        # NEED TO DO
        print("- Haven't implemented functionality")
        if SolarFlux_Model_Type == "FILE":
            if SolarFlux_File is not None:
                print("- Updating Solar Flux Model File")
                # NEED TO DO
                print("- Haven't implemented functionality")
            else:
                print("- No Solar Flux Model File specified, using default")
            if SolarFlux_Update_Rate is not None:
                print("- Updating Solar Flux Model Update Rate")
                # NEED TO DO
                print("- Haven't implemented functionality")
            else:
                print("- No Solar Flux Model Update Rate specified, using default")
        elif SolarFlux_Model_Type == "MANUAL_ENTRY":
            if SolarFlux_Avg is not None:
                print("- Updating Solar Flux Model Average Rate")
                # NEED TO DO
                print("- Haven't implemented functionality")
            else:
                print("- No Solar Flux Model Average Rate specified, using default")
            if SolarFlux_Daily is not None:
                print("- Updating Solar Flux Model Daily Rate")
                # NEED TO DO
                print("- Haven't implemented functionality")
            else:
                print("- No Solar Flux Model Daily Rate specified, using default")
    else:
        print("- No Solar Flux Model Type specified, using default")

    if Use_Apparent_Sun_Position is not None:
        more_options.drag.use_apparent_sun_position = Use_Apparent_Sun_Position
        print(f"- Updated use apparent sun position to {Use_Apparent_Sun_Position}")
    else:
        print("- No apparent sun position specified, using default")

    if Use_Approx_Altitude is not None:
        more_options.drag.use_approximate_altitude = Use_Approx_Altitude
        print(f"- Updated use approximate altitude to {Use_Approx_Altitude}")
    else:
        print("- No approximate altitude specified, using default")

    print("Finished updating drag settings")





"""
---------------------------
CentralBodyGravitySettings:
---------------------------
Defines the central body gravity settings for the HPOP simulation.
Handles setting changes on an input basis, such that certain settings are only changed if the user specifies a value for them.

INPUTS:

- force_model = Container for the settings to be changed. Comes from propagator.force_model. Contains central_body_gravity and more_options.
- max_degree = Maximum degree of the gravity model.
- max_order = Maximum order of the gravity model.

Optional:
- gravity_file = Path to an alternate gravity file.
- Use_SecularVariations = Boolean describing whether secular variations should be used.
- SolidTide_Type = Solid tide model type to be used. Settings required change depending on the type of model (NOT YET IMPLEMENTED).
    - Comes from SolidTide object
- Use_OceanTide = Boolean describing whether ocean tides should be used. All settings prefixed OceanTide are only accessed if true.
- OceanTide_max_degree = Maximum degree of ocean tide model.
- OceanTide_max_order = Maximum order of the ocean tide model.
- OceanTide_min_amplitude = Minimum amplitude of the ocean tide model.
"""

def CentralBodyGravitySettings(
    force_model,

    max_degree,
    max_order,
    gravity_file=None,
    Use_SecularVariation=False,

    SolidTide_Type=None,

    Use_OceanTide=False,
    OceanTide_max_degree=None,
    OceanTide_max_order=None,
    OceanTide_min_amplitude=None
):
    print("Updating Central Body Gravity Settings")
    
    central_body_gravity = force_model.central_body_gravity
    more_options = force_model.more_options

    central_body_gravity.set_maximum_degree_and_order(max_degree, max_order)
    print("- Set maximum degree and order of gravity model")

    if gravity_file is not None:
        # Haven't implemented yet
        print("- Updated gravity file")
        print("- Not implemented yet")
    else:
        print("- No gravity file specified, using default")

    if Use_SecularVariation:
        print("- Using secular variations of gravity model")
        central_body_gravity.use_secular_variations = Use_SecularVariation
    else:
        print("- Not using secular variations of gravity model")

    if SolidTide_Type is not None:
        central_body_gravity.solid_tide_type = SolidTide_Type
        print("- Updated solid tide type")
    else:
        print("- No Solid Tide Type specified, using default")

    central_body_gravity.use_ocean_tides = Use_OceanTide
    if Use_OceanTide == True:
        print("- Using ocean tides")
        if OceanTide_max_degree and OceanTide_max_order is not None:
            more_options.ocean_tides.maximum_degree = OceanTide_max_degree
            more_options.ocean_tides.maximum_order = OceanTide_max_order
            print("- Updated maximum degree and order of ocean tide model")
        else:
            print("- Either maximum degree or order of ocean tides not specified, using default")

        if OceanTide_min_amplitude is not None:
            more_options.ocean_tides.minimum_amplitude = OceanTide_min_amplitude
            print("- Updated minimum amplitude of ocean tide model")
        else:
            print("- No minimum amplitude of ocean tide model specified, using default")
    else:
        print("- Not using ocean tides")

    print("Finished updating central body gravity settings")





"""
-------------------------
ThirdBodyGravitySettings:
-------------------------
Chooses the third bodies that will be used in the propagation.

INPUTS:
- third_body_gravity = Settings object that will be edited. Comes from propagator.force_model.third_body_gravity
- add_bodies = Array of names of bodies as strings that should be added to the list of third bodies accounted for.
- remove_boides = Array of names as strings that should be removed if they are in the list.
"""

def ThirdBodyGravitySettings(third_body_gravity, add_bodies, remove_bodies):
    print("Updating third bodies")

    for body in add_bodies:
        third_body_gravity.add_third_body(body)
        print(f"- Added {body} to third bodies")
    
    for body in remove_bodies:
        third_body_gravity.remove_third_body(body)
        print(f"- Removed {body} from third bodies")
    
    print("Finished updating third bodies")





"""
-------------------------------
SolarRadiationPressureSettings:
-------------------------------
Updates the solar radiation pressure settings of the HPOP propagator.
Handles setting changes on an input basis, such that certain settings are only changed if the user specifies a value for them.

INPUTS:

- force_model = Container for the settings to be changed. Comes from propagator.force_model. Contains solar_radiation_pressure, eclipsing_bodies, and more_options.

Optional:
- SRP_Model = The solar radiation pressure model to be used. (Enum=SolarRadiationPressureModelType)
  - SRP_Cr = The coefficient of reflectivity of the satellite. Type=SPHERICAL
  - Area_Mass_Ratio = The area to mass ratio of the satellite. Type=SPHERICAL or Central_Body_RP
  - SRP_Scale = The scale factor for the solar radiation pressure. Type=GPS
  - SRP_y_bias = The y-bias for the solar radiation pressure. Type=GPS
- SRP_Boundary_Mitigation = The boundary mitigation method to be used.
- Add_Eclipsing_Bodies = The eclipsing bodies to be added.
- Remove_Eclipsing_Bodies = The eclipsing bodies to be removed.
- Shadow_Model = The shadow model to be used. (Enum=SolarRadiationPressureShadowModelType)
- Use_Central_Body_RP = Boolean describing whether the central body radiation pressure should be used.
  - Central_Albedo = The albedo of the central body.
  - Central_Thermal = The thermal radiation of the central body.
  - Ck = The coefficient of reflectivity of the satellite for central body radiation pressure.
  - Ground_Reflection_File = The ground reflection file to be used for central body radiation pressure.
- Atmosphere_Altitude = The altitude of the atmosphere for determining earths shape for eclipses.
- Sun_Position_Compute_Method = The method to be used for computing the position of the sun. (Enum=MethodToComputeSunPosition)
"""

def SolarRadiationPressureSettings(
    force_model,

    SRP_Model=None,
    SRP_Cr=None,
    Area_Mass_Ratio=None,
    SRP_Scale=None,
    SRP_y_bias=None,

    SRP_Boundary_Mitigation=None,

    Add_Eclipsing_Bodies=None,
    Remove_Eclipsing_Bodies=None,

    Shadow_Model=None,

    Use_Central_Body_RP=False,
    Use_Albedo=None,
    Use_Thermal=None,
    Ck=None,
    Ground_Reflection_File=None,

    Atmosphere_Altitude=None,
    Sun_Position_Compute_Method=None
):
    print("Updating solar radiation pressure settings")

    solar_radiation_pressure = force_model.solar_radiation_pressure
    eclipsing_bodies = force_model.eclipsing_bodies
    more_options = force_model.more_options

    solar_radiation_pressure.use = True

    if solar_radiation_pressure.solar_radiation_pressure_model.is_model_type_supported(SRP_Model) == True:
        solar_radiation_pressure.solar_radiation_pressure_model.set_model_type(SRP_Model)
        print(f"- Updated solar radiation pressure model to {SRP_Model}")
    else:
        print("- Invalid SRP model type specified, using default")

    model_name = str(SRP_Model).upper()

    if SRP_Model == "SPHERICAL":
        if SRP_Cr is not None:
            solar_radiation_pressure.solar_radiation_pressure_model.coefficient_of_reflectivity = SRP_Cr
            print(f"- Updated coefficient of reflectivity to {SRP_Cr}")
        else:
            print("- No coefficient of reflectivity specified, using default")

        if Area_Mass_Ratio is not None:
            solar_radiation_pressure.solar_radiation_pressure_model.area_mass_ratio = Area_Mass_Ratio
            print(f"- Updated area to mass ratio to {Area_Mass_Ratio}")
        else:
            print("- No area to mass ratio specified, using default")
    elif "GPS" in model_name:
        if SRP_Scale is not None:
            solar_radiation_pressure.solar_radiation_pressure_model.scale_factor = SRP_Scale
            print(f"- Updated scale factor to {SRP_Scale}")
        else:
            print("- No scale factor specified, using default")

        if SRP_y_bias is not None:
            solar_radiation_pressure.solar_radiation_pressure_model.y_bias = SRP_y_bias
            print(f"- Updated y-bias to {SRP_y_bias}")
        else:
            print("- No y-bias specified, using default")

    if SRP_Boundary_Mitigation is not None:
        solar_radiation_pressure.use_boundary_mitigation = SRP_Boundary_Mitigation
        print(f"- Updated boundary mitigation to {SRP_Boundary_Mitigation}")
    else:
        print("- No boundary mitigation specified, using default")

    for body in Remove_Eclipsing_Bodies:
        if eclipsing_bodies.is_eclipsing_body_assigned(body) == True:
            eclipsing_bodies.remove_eclipsing_body(body)
            print(f"- Removed {body} from eclipsing bodies")
        else:
            print(f"- {body} not in eclipsing bodies, cannot remove")

    for body in Add_Eclipsing_Bodies:
        if eclipsing_bodies.is_eclipsing_body_assigned(body) == False:
            eclipsing_bodies.add_eclipsing_body(body)
            print(f"- Added {body} to eclipsing bodies")
        else:
            print(f"- {body} already in eclipsing bodies, cannot add")

    if Shadow_Model is not None:
        solar_radiation_pressure.shadow_model = Shadow_Model
        print(f"- Updated shadow model to {Shadow_Model}")
    else:
        print("- No shadow model specified, using default")

    if Use_Central_Body_RP == True:
        if Use_Albedo is not None:
            more_options.radiation_pressure.include_albedo = Use_Albedo
            print(f"- Updated central body albedo to {Use_Albedo}")
        else:
            print("- No central body albedo specified, using default")

        if Use_Thermal is not None:
            more_options.radiation_pressure.include_thermal = Use_Thermal
            print(f"- Updated central body thermal to {Use_Thermal}")
        else:
            print("- No central body thermal specified, using default")

        if Ck is not None:
            more_options.radiation_pressure.ck = Ck
            print(f"- Updated central body coefficient of reflectivity to {Ck}")
        else:
            print("- No central body coefficient of reflectivity specified, using default")

        if Area_Mass_Ratio is not None:
            more_options.radiation_pressure.area_mass_ratio = Area_Mass_Ratio
            print(f"- Updated central body area to mass ratio to {Area_Mass_Ratio}")
        else:
            print("- No central body area to mass ratio specified, using default")

        if Ground_Reflection_File is not None:
            more_options.radiation_pressure.file = Ground_Reflection_File
            print(f"- Updated central body ground reflection file to {Ground_Reflection_File}")
        else:
            print("- No central body ground reflection file specified, using default")

    if Atmosphere_Altitude is not None:
        more_options.solar_radiation_pressure.atmosphere_altitude_of_earth_shape_for_eclipse = Atmosphere_Altitude
        print(f"- Updated atmosphere altitude to {Atmosphere_Altitude}")
    else:
        print("- No atmosphere altitude specified, using default")

    if Sun_Position_Compute_Method is not None:
        more_options.solar_radiation_pressure.method_to_compute_sun_position = Sun_Position_Compute_Method
        print(f"- Updated sun position compute method to {Sun_Position_Compute_Method}")
    else:
        print("- No sun position compute method specified, using default")

    print("Finished updating solar radiation pressure settings")





"""
----------------
GeneralForceSettings:
----------------
Updates certain general settings of the HPOP propagator.

INPUTS:

- more_options = Container for the settings to be changed. Comes from propagator.force_model.more_options.

Optional:
- Satellite_Mass = The mass of the satellite.
- Use_Relativistic_Acceleration = Boolean describing whether relativistic acceleration should be included.
"""

def GeneralForceSettings(
    more_options,

    Satellite_Mass=None,
    Use_Relativistic_Acceleration=None
):
    print("Updating general force settings")

    if Satellite_Mass is not None:
        more_options.static.satellite_mass = Satellite_Mass
        print(f"- Updated satellite mass to {Satellite_Mass}")
    else:
        print("- No satellite mass specified, using default")

    if Use_Relativistic_Acceleration is not None:
        more_options.static.include_relativistic_acceleration = Use_Relativistic_Acceleration
        print(f"- Updated use relativistic acceleration to {Use_Relativistic_Acceleration}")
    else:
        print("- No use relativistic acceleration specified, using default")

    print("Finished updating general force settings")