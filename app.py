#!flask/bin/python
from flask import Flask
import sectionproperties.pre.sections as sections
from sectionproperties.analysis.cross_section import CrossSection

app = Flask(__name__)

@app.route('/')
def index():
  return "Hello, World!"

@app.route('/navier/api/v1.0/properties', methods=['GET'])
def get_properties():

  # build the lists of points, facets, holes and control points
  points = request.json['points']
  facets = request.json['facets']
  holes = request.json['holes']
  control_points = request.json['controls']

  # create the custom geometry object
  geometry = sections.CustomSection(points, facets, holes, control_points)
  geometry.clean_geometry()  # clean the geometry

  # create the mesh - use a smaller refinement for the angle region
  mesh = geometry.create_mesh(mesh_sizes=[0.0005, 0.001])

  # create a CrossSection object
  section = CrossSection(geometry, mesh)

  # perform a geometric, warping and plastic analysis
  section.calculate_geometric_properties()
  section.calculate_warping_properties()
  section.calculate_plastic_properties()

  properties = section.display_results()

  return jsonify({'properties': properties})

if __name__ == '__main__':
  app.run(debug=True)