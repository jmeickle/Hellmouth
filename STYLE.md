# Code style in Unicursal

## Imports

Imports should be grouped according to this extension of the [PEP-8 guidelines on imports](http://www.python.org/dev/peps/pep-0008/#imports).

- First-party Python libraries (e.g., 'import curses')

- Third-party Python libraries (e.g., 'import gevent')

- Unicursal library imports
  - Imports from src.lib.core.*
  - Imports from anything else
  - Imports from src.lib.util.*

- Game library imports

- Unicursal data imports

- Game data imports