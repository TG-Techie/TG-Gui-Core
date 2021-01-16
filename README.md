# TG-Gui-Core

TG-Gui-Core is the code shared between platforms used to build standard library

This module includes the definitions of Widget, Container, and Layout along with the abstractions used to make placing and constructing widgets easier.

## Usage Notes
This module is not meant to be used on its own, It generally requires an implementation of the TG-Gui Standard Library (TODO: add link to Std Library template).

When combined with a standard library, user interfaces can be easily defined.
```python
from tg_gui_std import *

@appwrapper
class MyApp(Layout):
    """
    A window split in half, the bottom prints out a greeting when clicked and
        the top says hello to the user.
        +------------+
        | [greeting] |
        | [greeter]  |
        +------------+
    """

    greeting = Label(text="Hi!")
    greeter = Button(text="print greeting?", press=self.on_press)

    def _any_(self):
        half = (self.width, self.height//2)
        greeting = self.greeting((left, top), half)
        greeter = self.greeter(below(greeting), half)

    def on_press(self):
        print("Who would wish to cross the "\
            +"bridge of death must answer me"\
            +"these questions three..."
        )
```
## Dependencies
- Python3.5+ or circuitpython 6.0+
