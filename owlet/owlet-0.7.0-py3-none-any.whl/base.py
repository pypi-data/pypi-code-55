import owlet

x = owlet.read_egf("/Users/henryiii/Documents/GitHub/owlet/excluded/egf_examples/PostOfficeSquare.egf")

# owlet.visualize(x)
my_shape = owlet.read_csv("/Users/henryiii/Documents/GitHub/owlet/excluded/PostOfficeSquare_Boundary.csv")

owlet.write_kml(path, my_shape, 'Park Name', 'Parks', altitude_mode='rtg')
# owlet.write_kml("/Users/henryiii/Documents/GitHub/owlet/excluded/PostOfficeSquare_Boundary.kml", x, 'Park Name', 'Parks')