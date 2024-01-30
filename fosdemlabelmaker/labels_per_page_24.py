import labels
from reportlab.graphics import shapes
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont, stringWidth
from os.path import join, exists


class LabelsPerPage24:
    """
    Generate 24 labels per page.
    Built for Avery Zweckform L4773-20.
    """
    specs = {
        'sheet_width': 210,
        'sheet_height': 297,
        'columns': 3,
        'rows': 8,
        'label_width': 63.5,
        'label_height': 33.9,
        'left_margin': 7,
        'top_margin': 13,
        'row_gap': 0,
        'column_gap': 3
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

        while item_counter < first_item + 24:
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
        Generate 24 item labels for a single box.
        Returns the first unused label (so don't increment or you'll have a gap).
        """
        def draw_label(label, width, height, data):
            label.add(shapes.Image(-2, 40, 50, 50, path='img/gear_w_bg.png'))
            label.add(shapes.String(58, 75, 'Property of', fontName='Source Sans Pro', fontSize=12))
            label.add(shapes.String(58, 55, 'FOSDEM', fontName='Source Sans Pro', fontSize=14))
            label.add(shapes.String(-2, 10, data['id'], fontName='Source Code Pro', fontSize=30))
            label.add(shapes.Image(117, 35, 60, 60, path=data['qr_path']))
        
        def mk_id(item):
            return 'B{0}I{1}'.format(
                str(box).rjust(3, '0'),
                str(item).rjust(5, '0')
            )
        
        def mk_out(first_item, current_item):
            return '{0}_{1}-{2}_24.pdf'.format(
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
            label.add(shapes.String(0, 20, data['building'].upper(), fontName='Source Code Pro', fontSize=100))
            label.add(shapes.Image(70, 40, 50, 50, path='img/gear_w_bg.png'))
            label.add(shapes.String(70, 10, data['id'], fontName='Source Code Pro', fontSize=30))
            label.add(shapes.Image(117, 35, 60, 60, path=data['qr_path']))
        
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
            return '{0}_{1}-{2}_24.pdf'.format(
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
