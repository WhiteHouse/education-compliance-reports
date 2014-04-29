#!/usr/bin/python2.7

# Python program for changing the consentagreements.csv into useable geojson

with open('consentagreements.csv', 'r') as csv_file:
    text = csv_file.read().strip().split('\n')

header_row = text[0].split(',')

dictionary = {}

for row, line in enumerate(text[1:]):

    dictionary[row] = {}

    for col, cell in enumerate(line.split(',')):

        dictionary[row][header_row[col]] = cell

geojson = []

for row in dictionary.keys():
    geojson.append('  {')

    geometry = ['0','0']
    properties = []
    address = ['','','']

    for column, cell in dictionary[row].items():

        if cell.strip() == '':
            cell = '" "'

        if column == '"Latitude"':
            geometry[1] = '\t {0}'.format(cell)
        elif column == '"Longitude"':
            geometry[0] = '\t {0}'.format(cell)
        elif column == '"City"':
            address[0] = cell
        elif column == '"State"':
            address[1] = cell
        elif column == '"Zip"':
            address[2] = cell
        elif column == '"Title"':
            properties.append('      "name": {0},'.format(cell))
        else:
            properties.append('      {0}: {1},'.format(column, cell))

    geojson.append('   "type": "Feature",')
    geojson.append('   "geometry": {')
    geojson.append('      "type": "Point",')
    geojson.append('      "coordinates": [')
    geojson.append(',\n'.join(geometry))
    geojson.append('    \t]')
    geojson.append('    },')
    geojson.append('    "properties": {')
    geojson.append('      "marker-symbol": "marker",')
    geojson.append('      "marker-color": "#D4500F",')
    geojson.append('      "address": "{0}",'.format(' '.join(address).replace('"','')))

    # Remove trailing comma from last item in properties
    last = properties.pop()
    properties.append(last[:-1])

    geojson.extend(properties)
    geojson.append('      }')

    geojson.append('  },\n')

# Remove trailing commas from last item in geojson

geojson.pop()
geojson.append('  }\n')

# Create prefix and suffix to wrap around all features to make it .geojson

prefix = '''
{
  "type": "FeatureCollection",
  "features": [
'''

suffix = '''
  ]
}
'''

geojson.insert(0, prefix)
geojson.append(suffix)

with open('consentagreements.json', 'w') as geojson_file:
    geojson_file.write('\n'.join(geojson))