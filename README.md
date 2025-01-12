# fosdem-label-generator
A label generator for FOSDEM.

This rusty implement can be used to generate item labels for FOSDEM things.
It supports:

* Avery Zweckform L4773-20 (24 labels per page)
* Avery Zweckform L4778-20 (48 labels per page)

It spits out a PDF of A4's that you can print on any laser printer. When printing
do not set the *fit to paper* or *scale* options, as the margins are set in the
PDF to the correct dimensions.

## Installation

* Download the code.
* Install the requirements (`pip install -r requirements.txt --user`) (requires Python 3).

## Usage

* Generates pages of labels.
* Generates the QR-codes automatically (`{}`).
* Output is in `out/labels` (PDF with labels) and `out/qr-codes` (QR codes).

### Generic options

| Option | Usage |
|--------|-------|
| `--box` | Number of the box to generate a label page for. |
| `--first_item` | Number of the first label that will be generated. To get the next item for a new page, add 24 or 48. Items start at 1. |
| `--building` | Name (1 letter) of the building to generate a label page for. AW is not supported. |
| `--room` | Name of the room (`$building$floor.$room`) to generate a label page for. |

### Types of label
*The parameter `--first_item` is always required.*

#### 24 labels per page (L4773-20)
* Items that go in a box: `--24_labels_box`. Requires `--box`.
* Items that go in a building: `--24_labels_building`. Requires `--building`.

#### 48 labels per page (L4778-20)
* Items that go in a box: `--48_labels_box`. Requires `--box`.
* Items that go in a building: `--48_labels_building`. Requires `--building`.
* Items that go in a room (generates 8 labels per room): `--48_labels_room`. Requires `--room`.
