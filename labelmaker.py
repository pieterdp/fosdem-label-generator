import argparse
from fosdemlabelmaker.qr_codes import QRCodeGenerator
from fosdemlabelmaker.labels_per_page_24 import LabelsPerPage24
from fosdemlabelmaker.labels_per_page_48 import LabelsPerPage48
from fosdemlabelmaker.rooms_generator import RoomsGenerator


def check_req_params(args, params):
    for param in params:
        if not getattr(args, param, None):
            raise Exception('Parameter {0} is required.'.format(param))


def main():
    parser = argparse.ArgumentParser(
        prog='FOSDEMItemLabeler',
        description='Generate labels for FOSDEM items'
    )
    parser.add_argument('--24_labels_box', action='store_true', help='Generate a page with 24 labels for items in --box. Requires --first_item and --box.')
    parser.add_argument('--24_labels_building', action='store_true', help='Generate a page with 24 labels for items that should go to --building. Requires --first_item and --building.')
    parser.add_argument('--48_labels_box', action='store_true', help='Generate a page with 48 labels for items in --box. Requires --first_item and --box.')
    parser.add_argument('--48_labels_building', action='store_true', help='Generate a page with 48 labels for items that should go to --building. Requires --first_item and --building.')
    parser.add_argument('--48_labels_room', action='store_true', help='Generate a page with 48 labels for items that should go to a room. 8 labels per room. Requires --first_item.')

    parser.add_argument('--box', help='Number of the box.', type=int)
    parser.add_argument('--building', help='Building for the item labels.')
    parser.add_argument('--first_item', help='Number of the first item on the first label.', type=int)

    args = parser.parse_args()

    qr_generator = QRCodeGenerator()

    if getattr(args, '24_labels_box', None):
        labelmaker = LabelsPerPage24()
        check_req_params(args, ['box', 'first_item'])
        print('Generating 24 labels between {0} and {1} for box {2} ... '.format(
            args.first_item,
            args.first_item + 24 - 1,
            args.box
        ))
        item = args.first_item
        while item < args.first_item + 48:
            qr_generator.generate_for_item(
                item,
                box=args.box
            )
            item += 1
        labelmaker.generate_item_labels_for_box(
            args.box,
            args.first_item
        )
        return 0

    elif getattr(args, '24_labels_building', None):
        labelmaker = LabelsPerPage24()
        check_req_params(args, ['building', 'first_item'])
        print('Generating 24 labels between {0} and {1} for building {2} ... '.format(
            args.first_item,
            args.first_item + 24 - 1,
            args.building
        ))
        item = args.first_item
        while item < args.first_item + 24:
            qr_generator.generate_for_item(
                item,
                destination=args.building
            )
            item += 1
        labelmaker.generate_item_labels_for_building(
            args.building,
            args.first_item
        )
        return 0
    elif getattr(args, '48_labels_box', None):
        labelmaker = LabelsPerPage48()
        check_req_params(args, ['box', 'first_item'])
        print('Generating 48 labels between {0} and {1} for box {2} ... '.format(
            args.first_item,
            args.first_item + 48 - 1,
            args.box
        ))
        item = args.first_item
        while item < args.first_item + 48:
            qr_generator.generate_for_item(
                item,
                box=args.box
            )
            item += 1
        labelmaker.generate_item_labels_for_box(
            args.box,
            args.first_item
        )
        return 0
    elif getattr(args, '48_labels_building', None):
        labelmaker = LabelsPerPage48()
        check_req_params(args, ['building', 'first_item'])
        print('Generating 48 labels between {0} and {1} for building {2} ... '.format(
            args.first_item,
            args.first_item + 48 - 1,
            args.building
        ))
        item = args.first_item
        while item < args.first_item + 48:
            qr_generator.generate_for_item(
                item,
                destination=args.building
            )
            item += 1
        labelmaker.generate_item_labels_for_building(
            args.building,
            args.first_item
        )
        return 0
    elif getattr(args, '48_labels_room', None):
        labelmaker = LabelsPerPage48()
        check_req_params(args, ['first_item'])
        roomgenerator = RoomsGenerator()

        print('Generating sets of 48 labels between {0} and {1} for all rooms (8 per room) ... '.format(
            args.first_item,
            (roomgenerator.total * 8) + args.first_item - 1
        ))
        item = args.first_item
        rooms_total = roomgenerator.total
        counter = 0
        
        while item < args.first_item + rooms_total * 8:
            for building, room in roomgenerator.rooms_as_list:
                items_in_room = 1
                while items_in_room <= 8:
                    qr_generator.generate_for_item(
                        item,
                        destination=room
                    )
                    item += 1
                    items_in_room += 1
        
        labelmaker.generate_item_labels_for_rooms(
            roomgenerator.rooms_as_list,
            args.first_item
        )
        return 0

    return 0


if __name__ == '__main__':
    exit(main())
