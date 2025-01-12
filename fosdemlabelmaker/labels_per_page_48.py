import labels
from reportlab.graphics import shapes
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont, stringWidth
from os.path import join, exists


class LabelsPerPage48:
    """
    Generate 48 labels per page.
    Built for Avery Zweckform L4778-20.
    """
    specs = {
        'sheet_width': 210,
        'sheet_height': 297,
        'columns': 4,
        'rows': 12,
        'label_width': 45.7,
        'label_height': 21.2,
        'left_margin': 10,
        'top_margin': 21.5,
        'row_gap': 0,
        'column_gap': 2.5
    }

    def __init__(self, qr_loc='out/qr-codes', output_loc='out/labels'):
        # Fonts
        registerFont(TTFont('Source Code Pro', 'fonts/SourceCodePro-Regular.ttf'))
        registerFont(TTFont('Source Sans Pro', 'fonts/SourceSans3-Regular.ttf'))
        # Set up of the label maker
        self.sheet_specs = labels.Specification(**self.specs)
        # QR code location
        self.qr_loc = qr_loc
        # Output location
        self.out_loc = output_loc
    

    def _generic_label_generator(self, first_item, id_cb, out_cb, label_cb, data_cb=None):
        """
        Generic label generator.
        """
        sheet = labels.Sheet(self.sheet_specs, label_cb, border=False)

        item_counter = first_item

        while item_counter < first_item + 48:
            item_id = id_cb(item_counter)
            if data_cb:
                payload = data_cb(item_id, item_counter)
            else:
                payload = {
                    'id': item_id,
                    'item': item_counter,
                    'qr_path': join(self.qr_loc, '{0}.png'.format(item_counter))
                }
            sheet.add_label(payload)
            item_counter += 1
        
        out_filename = out_cb(first_item, item_counter)

        sheet.save(
            join(self.out_loc, out_filename)
        )

        return item_counter
            
    
    def generate_item_labels_for_box(self, box, first_item):
        """
        Generate 48 item labels for a single box.
        Returns the first unused label (so don't increment or you'll have a gap).
        """
        def draw_label(label, width, height, data):
            #label.add(shapes.Image(-2, 35, 25, 25, path='img/gear_w_bg.png'))
            label.add(shapes.Image(-2, 35, 25, 25, path='img/fosdem_logo_gerry.png'))
            label.add(shapes.String(30, 50, 'Property of', fontName='Source Sans Pro', fontSize=8))
            label.add(shapes.String(30, 40, 'FOSDEM', fontName='Source Sans Pro', fontSize=8))
            label.add(shapes.String(-2, 5, data['id'], fontName='Source Code Pro', fontSize=20))
            label.add(shapes.Image(80, 20, 40, 40, path=data['qr_path']))
        
        def mk_id(item):
            return 'B{0}I{1}'.format(
                str(box).rjust(3, '0'),
                str(item).rjust(5, '0')
            )
        
        def mk_out(first_item, current_item):
            return '{0}_{1}-{2}_48.pdf'.format(
            box,
            first_item,
            current_item - 1
        )
        
        return self._generic_label_generator(
            first_item,
            mk_id,
            mk_out,
            draw_label
        )
    
    
    def generate_item_labels_for_building(self, building, first_item):
        """
        Generate item labels for things that belong in a building, but are not in a box.
        """
        def draw_label(label, width, height, data):
            label.add(shapes.Image(-2, 35, 25, 25, path='img/gear_w_bg.png'))
            label.add(shapes.String(0, 20, data['building'].upper(), fontName='Source Code Pro', fontSize=60))
            label.add(shapes.String(-2, 5, data['id'], fontName='Source Code Pro', fontSize=20))
            label.add(shapes.Image(80, 20, 40, 40, path=data['qr_path']))
        
        def mk_data(item_id, item_counter):
            payload = {
                'id': item_id,
                'item': item_counter,
                'building': building,
                'qr_path': join(self.qr_loc, '{0}.png'.format(item_counter))
            }
            return payload

        def mk_id(item):
            return 'I{0}'.format(
                str(item).rjust(5, '0')
            )
        
        def mk_out(first_item, current_item):
            return '{0}_{1}-{2}_48.pdf'.format(
            building,
            first_item,
            current_item - 1
        )
        
        return self._generic_label_generator(
            first_item,
            mk_id,
            mk_out,
            draw_label,
            mk_data
        )
    
    def generate_item_labels_for_rooms(self, room_list, first_item):
        """
        Generate labels for items that should go to a specific room.
        room_list = [(building, room)]
        8 labels per room
        """
        def label_cb(label, width, height, data):
            label.add(shapes.String(0, 35, data['room'].upper(), fontName='Source Code Pro', fontSize=22))
            label.add(shapes.String(-2, 5, data['id'], fontName='Source Code Pro', fontSize=18))
            label.add(shapes.Image(92, 0, 35, 35, path=data['qr_path']))
            label.add(shapes.Image(70, 0, 25, 25, path='img/gear_w_bg.png'))

        sheet = labels.Sheet(self.sheet_specs, label_cb, border=False)

        item_counter = first_item
        rooms_total = len(room_list)

        while item_counter < first_item + rooms_total * 8:
            for building, room in room_list:
                items_in_room = 1
                while items_in_room <= 8:
                    item_id = 'I{0}'.format(
                        str(item_counter).rjust(5, '0')
                    )
                    payload = {
                        'id': item_id,
                        'room': room,
                        'item': item_counter,
                        'qr_path': join(self.qr_loc, '{0}.png'.format(item_counter))
                    }
                    sheet.add_label(payload)
                    item_counter += 1
                    items_in_room += 1
        
        out_filename = 'ROOMS_{0}_{1}-{2}_48.pdf'.format(
            building,
            first_item,
            item_counter - 1
        )

        sheet.save(
            join(self.out_loc, out_filename)
        )

        return item_counter

