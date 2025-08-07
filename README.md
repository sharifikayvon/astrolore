# Astrolore

This package, given the name of any astrophysical object, finds the nearest source that has been referenced in science fiction. There are options to 1) observe
the nearest sci-fi source in the [Aladin Sky Atlas](https://aladin.cds.unistra.fr/AladinLite/) and 2) generate a sky plot showing the separation between the input object and nearest sci-fi source.

![alt text]([https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png](https://github.com/sharifikayvon/astrolore/blob/develop_arnab/Readme_img.png))


### Installation

This package can be pip installed.

```
pip install astrolore
```

#### Dependencies
* pandas
* astropy
* numpy
* matplotlib
* pywebview
* tkinter

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





