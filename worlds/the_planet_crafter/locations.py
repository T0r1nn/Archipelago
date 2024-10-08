location_start_id = 1284190

names = [
    "CraftStation2",
    "WallWindow",
    "FloorGlass",
    "Vegetube2",
    "VegetubeOutside1",
    "Drill1",
    "Drill2",
    "Drill3",
    "Drill4",
    "EnergyGenerator2",
    "EnergyGenerator3",
    "EnergyGenerator4",
    "EnergyGenerator5",
    "EnergyGenerator6",
    "ScreenTerraStage",
    "Container2",
    "Backpack2",
    "Backpack3",
    "Backpack5",
    "Backpack6",
    "OxygenTank2",
    "OxygenTank3",
    "EquipmentIncrease2",
    "EquipmentIncrease3",
    "EquipmentIncrease4",
    "PulsarQuartz",
    "Seed0",
    "Heater2",
    "Heater3",
    "Heater4",
    "Heater5",
    "FabricBlue",
    "BedDouble",
    "Beacon1",
    "ComAntenna",
    "ScreenMessages",
    "Rod-alloy",
    "Rod-osmium",
    "Ladder",
    "OreExtractor1",
    "OreExtractor2",
    "OreExtractor3",
    "VegetableGrower1",
    "VegetableGrower2",
    "WaterCollector1",
    "GrassSpreader1",
    "SeedSpreader1",
    "SeedSpreader2",
    "Biolab",
    "AlgaeSpreader1",
    "AlgaeSpreader2",
    "WaterFilter",
    "Biodome1",
    "Biodome2",
    "ButterflyDome1",
    "WaterCollector2",
    "Jetpack4",
    "FusionEnergyCell",
    "RocketBiomass1",
    "RocketOxygen1",
    "RocketInsects1",
    "GasExtractor1",
    "GasExtractor2",
    "Mutagen2",
    "Mutagen3",
    "Mutagen4",
    "GeneticManipulator1",
    "ScreenRockets",
    "Tree3Seed",
    "Tree4Seed",
    "Tree5Seed",
    "Tree6Seed",
    "Tree9Seed",
    "Sign",
    "FlowerPot1",
    "TreeSpreader0",
    "TreeSpreader1",
    "TreeSpreader2",
    "Teleporter1",
    "Incubator1",
    "LarvaeBase1",
    "ScreenBiomass",
    "Beehive1",
    "Butterfly8Larvae",
    "Butterfly9Larvae",
    "Butterfly10Larvae",
    "Beehive2",
    "Farm1",
    "SilkGenerator",
    "ButterflyFarm1",
    "LarvaeBase3",
    "ButterflyDisplayer1",
    "Butterfly16Larvae",
    "Butterfly17Larvae",
    "AstroFood2",
    "AirFilter1",
    "AutoCrafter1",
    "ButterflyFarm2",
    "DroneStation1",
    "WaterLifeCollector1",
    "Fish1Eggs",
    "Fish3Eggs",
    "Fish5Eggs",
    "Fish6Eggs",
    "FishDisplayer1",
    "FrogDisplayer1",
    "CircuitBoard1",
    "Aquarium1",
    "Aquarium2",
    "FishFarm1",
    "AmphibiansFarm1",
    "Frog1Eggs",
    "Frog2Eggs",
    "Frog9Eggs",
    "Frog7Eggs",
    "Frog5Eggs",
    "Frog4Eggs",
    "Optimizer1",
    "Optimizer2",
    "GeneticExtractor1",
    "GeneticSynthetizer1",
    "LaunchPlatform",
    "PortalGenerator1",
    "PinChip1",
    "AnimalShelter1",
    "AnimalFeeder1",
    "DeparturePlatform",
    "RocketAnimals1",
    "Ecosystem1",
    "AnimalFood1",
    "AnimalFood2"
]

heat = []
pressure = []
oxygen = []
terraformation = []

plants = []
insects = []
animals = []
biomass = []

chips = []


def generate_location_map():
    location_id = location_start_id
    location_map = {}
    for location_name in names:
        location_map[location_name] = location_id
        location_id += 1
    return location_map
