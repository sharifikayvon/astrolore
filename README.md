# Astrolore

This package, given the name of any astrophysical object, finds the nearest source that has been referenced in science fiction. There are options to 1) observe
the nearest sci-fi source in the [Aladin Sky Atlas](https://aladin.cds.unistra.fr/AladinLite/) and 2) generate a sky plot showing the separation between the input object and nearest sci-fi source.


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
<div align="center">
  <img width="528" height="416" alt="image" src="https://github.com/user-attachments/assets/3b48d0e0-c7f1-4351-abbb-ee5d91de5f38" />
</div>

### Authors:

* Arnab Lahiry (alahiry@ics.forth.gr)
* Isabele Souza Vitorio (ivitorio@umich.edu)
* Joe Adamo (jadamo@arizona.edu)
* Kayvon Sharifi (ksharifi1@gsu.edu)






