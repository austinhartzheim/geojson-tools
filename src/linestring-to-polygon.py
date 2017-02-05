#! /usr/bin/env python3
'''
Tool to convert a simple linestring to a polygon.
'''
import argparse
import geojson


class Main():
    def __init__(self, args):
        self.args = args

    def convert(self):
        data = geojson.load(self.args.infile)
        for feature in data['features']:
            # Only operate on LineString features
            if not isinstance(feature.geometry, geojson.geometry.LineString):
                continue

            print('Processing LineString')  # TODO: remove debug

            # Only operate on LineStrings with >= 4 coordinates
            # TODO: we may be able to operate on LineStrings with 3 coordinates
            #   in some situations by ensuring that we add the 4th, duplicate
            #   coordinate which closes the shape.
            coordinates = feature.geometry.coordinates
            if len(coordinates) < 4:
                continue

            # TODO: check if first and last coordinates are the same.
            #   Add an argument to allow forcing this.
            assert(len(coordinates) > 3)
            if coordinates[0] != coordinates[-1]:
                # If --force-close was passed, force this LineString to be
                #   a complete, closed shape.
                if self.args.force_close:
                    coordinates.append(coordinates[0])

                else:
                    print('Skipping un-closed shape.')
                    print('  Pass --force-close to change this.')
                    continue

            polygon = geojson.geometry.Polygon([coordinates])
            if not geojson.is_valid(polygon):
                # TODO: handle this case.
                print('Generated polygon is invalid.')
            feature.geometry = polygon

        geojson.dump(data, self.args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outfile', type=argparse.FileType('w'))
    parser.add_argument('--force-close', action='store_true',
                        help='Force-close lines (creating a full loop/area)')
    args = parser.parse_args()

    main = Main(args)
    main.convert()
