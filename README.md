# TG-Gui-Core

TG-Gui a framework intended to make developing UI easy, intuitive, and enjoyable.

## Usage Notes
This module is the core foundation for the TG-Gui framework and is a building block for libraries of widgets.

## Example Usage
```python
from tg_gui_std._all_ import *
from datetime import datetime

@singleinstance
class Application(Layout):

    greeting = Label("hello, world!")
    our_button = Button("print the time", action=self.print_current_time())

    def _any_(self):
        """place the label and button inside of our layout ("Application")"""
        # calculate the label and button size to be full width and half height
        size = (self.width, self.height//2)
        # place the widgets
        greeting = self.greeting(top, size)
        our_button = self.our_button(below(greeting), size)

    def print_current_time(self):
        print(f"the current time is {datetime.now()}")
```

## Dependencies
- Python3.5+ or circuitpython 6.0+
- Most usage will also require a standard library of widget, this is currently under development
- python black

# Contributing
### Behavior
[Insert code of conduct link here once decided]

However, In Short:
- be nice
- don't discriminate
- work together
- understand people make mistakes

### Code

- Using should not require understanding
- Disclose complexity progressively
- Use sugar to make code easier to read (not to write)
- Only infer on top of what is already explicit
- The fewer ways a value needs to be checked, the better
- Well written code won't be well written until it is done, so add comments
- Run ``python -c "import this"``
- If you can't read it, re-write it (cause neither can I)
