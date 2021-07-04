# Genea

Pronounced "genie". Scrape parent-child relationships from Wikipedia infoboxes.

## Installation

Clone this repository to your local machine with git, then install with Python.

```bash
git clone https://github.com/shanedrabing/genea.git
cd genea
python setup.py install
```

## Getting Started

Run the program with Python.

```bash
python genea.py 'George Washington' '^Parent' '^Child'
```

### Positional arguments

- `term` : Search term. Leads to initial Wikipedia page.
- `pre` : Optional, regex. If matched, will add ancestor.
- `post` : Optional, regex. If matched, will add descendant.
- `extra` : Optional, regex. If matched, will add additional links (no
  relation).

### Optional arguments

- `-n` : How many cycles to walk from initial page?

## Example Output

```txt
ANCESTORS of George Washington
├── Augustine Washington Sr.  
│   ├── Mildred Gale
│   │   └── Augustine Warner Jr.
│   │       └── Augustine Warner
│   └── Lawrence Washington
│       └── John Washington
│           └── Lawrence Washington
└── Mary Washington

DESCENDANTS of George Washington
└── John Parke Custis
    ├── George Washington Parke Custis
    │   ├── Mary Anna Custis Lee
    │   │   ├── Eleanor Agnes Lee
    │   │   ├── George Washington Custis Lee
    │   │   ├── William Henry Fitzhugh Lee
    │   │   ├── Robert E. Lee Jr.
    │   │   ├── Mildred Childe Lee
    │   │   ├── Anne Carter Lee
    │   │   └── Mary Custis Lee
    │   └── Maria Carter Syphax
    ├── Martha Parke Custis Peter
    ├── Elizabeth Custis Law
    └── Eleanor Parke Custis Lewis
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
