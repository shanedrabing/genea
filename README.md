# Genea

Pronounced "genie". Scrape parent-child relationships from Wikipedia infoboxes.

## Installation

Clone this repository to your local machine with git, then install with Python.

```bash
git clone https://github.com/shanedrabing/genea.git
cd genea
python setup.py install
```

## Why Infoboxes?

<p align="center">
  <img src="docs/infobox_washington.png" alt="infobox_washington.png"/>
  <i>
    Modification of infobox as seen on
    <a href="https://en.wikipedia.org/wiki/George_Washington">
        Wikipedia page for George Washington
    </a>
  </i>
</p>

Infoboxes give us a digest of a particular Wikipedia page, alongside the
relational information we need to build a tree. In the image above, we can see
rows of information under the "Personal Details" section; each of these rows
contain a header (bolded text) and (usually) associated links.

We'll use regular expression patterns to match with these headers, some of
which provide ancestral relationships ("Parents", in this case), some provide
descendant relationships ("Children"), and others that could provide extra
links that we can walk out from ("Relatives").

Let's try this example.

## Getting Started

Run the program with Python.

```bash
python genea.py 'George Washington' '^Parent' '^Child' '^Relative'
```

### Positional arguments

- `term` : Search term. Redirects to initial Wikipedia page.
- `pre` : (optional, regex) If matched, will add ancestor.
- `post` : (optional, regex) If matched, will add descendant.
- `extra` : (optional, regex) If matched, will add additional links (no
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
