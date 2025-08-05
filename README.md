# astrolore

This package, given the name of any astrophysical object, finds the nearest source that has been referenced in science fiction. There is an option to launch your browser to "observe" 
the nearest sci-fi source in the [Aladin Sky Atlas](https://aladin.cds.unistra.fr/AladinLite/)

### Installation

This package can be pip installed. The PyPI page can be found [here](https://youtu.be/dQw4w9WgXcQ?si=PrA9bHia6hlaMwB-)

```
pip install astrolore
```

#### Dependencies
* pandas
* astropy
* numpy

### Running the code

```python
import astrolore

obj_name = 'Pleiades'

astrolore.closest_star_finder(obj_name)
```

### Authors:

* Arnab Lahiry (alahiry@ics.forth.gr)
* Isabele Souza Vitorio (ivitorio@umich.edu)
* Joe Adamo (jadamo@arizona.edu)
* Kayvon Sharifi (ksharifi1@gsu.edu)
