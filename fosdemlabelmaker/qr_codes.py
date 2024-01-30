import qrcode
import json
from os import makedirs
from os.path import join, exists


class QRCodeGenerator:
    """
    Generate QR codes for FOSDEM purposes.
    """
    inventory_base_url = 'https://inventory.fosdem.org/link'

    def generate_for_item(self, item, qr_loc='out/qr-codes', destination=None, storage=None, box=None):
        """
        Generate a QR code for a FOSDEM item
        """
        qr_code_data = {
            'item': item,
            'link': '{0}/{1}'.format(
                self.inventory_base_url,
                item
            ),
            'destination': destination,
            'storage': storage,
            'box': box
        }

        if not exists(qr_loc):
            makedirs(qr_loc)
        
        payload = json.dumps(qr_code_data)

        img = qrcode.make(payload)

        img.save(join(qr_loc, '{0}.png'.format(item)))

        return qr_code_data

