from astrolore.dataset import astrolore_dataset

def test_find_nearest_object_given_name_in_catalog():

    dataset = astrolore_dataset()

    # give it a name that is in the dataset
    test_name = "andromeda"
    closest_object = dataset.find_closest_object(test_name)
    assert closest_object["name"].lower() == test_name.lower()

    test_name = "Andromeda"
    closest_object = dataset.find_closest_object(test_name)
    assert closest_object["name"].lower() == test_name.lower()

    test_name = "ANDROMEDA"
    closest_object = dataset.find_closest_object(test_name)
    assert closest_object["name"].lower() == test_name.lower()

def test_find_nearest_object_given_name_not_in_catalog():

    dataset = astrolore_dataset()

    # give it a name that is in the dataset
    test_name = "SDSS J121700.14+151610.4"
    closest_name = "theta leonis"
    closest_object = dataset.find_closest_object(test_name)
    assert closest_object["name"].lower() == closest_name.lower()

def test_find_nearest_object_given_coords():
    pass