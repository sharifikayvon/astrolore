import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
import webbrowser
import os
import numpy as np
import matplotlib.pyplot as plt

class astrolore_dataset():
    """This class contains the dataset of astronomical objects in science fiction properties,
    and several methods for accesing and manipulating said dataset
    """
    def __init__(self):
        """Class constructor, loads in data from csv file"""
        path = os.path.dirname(__file__)
        self.scifi_dataframe = pd.read_csv(os.path.join(path, "data", "scifi_dataset.csv"))
        

    @staticmethod
    def format_sources(sources:list):
        """Formats output of sci-fi sources
        e.g. instead of 'Star Trek, Star Wars, Dune', output 'Star Trek, Star Wars, and Dune'

        Args:
            sources (list): list of sci-fi sources, e.g. '(Star Trek, Star Wars, Dune)'

        Returns:
            string: formatted sci-fi sources
        """
        if not sources:
            return ""
        elif len(sources) == 1:
            return sources[0]
        elif len(sources) == 2:
            return f"{sources[0]} and {sources[1]}"
        else:
            return f"{', '.join(sources[:-1])}, and {sources[-1]}"

    @staticmethod
    def get_coords_from_name(name):
        return SkyCoord.from_name(name)
    
    def name_of_object(self, object):
        if isinstance(object, pd.Series):
            return object["name"]
        else:
            raise ValueError

    def index_of_object(self, object):

        if isinstance(object, str):
            names = list(self.scifi_dataframe["name"])
            idx = names.index(object)
        elif isinstance(object, pd.Series):
            raise NotImplementedError
        else:
            raise ValueError

        return idx

    def find_closest_object(self, name:str = None, coords=None):
        """Given either an input identifier, e.g. Arcturus, or coordinates (RA, DEC), this function searches the scifi_dataset 
        for the sci-fi source with the smallest angular separation

        Args:
            name (string, optional): . Defaults to None.
            coords (tuple, optional): tuple of RA+DEC strings in format ('00h00m00s', '00d00m00s'). Defaults to None.

        Returns:
            close_object (pandas df)
        """        
        
        if name is None:
            name = 'Andromeda'

        if coords is None:
            self.user_coords = self.get_coords_from_name(name)           
        else:
            ra, dec = coords
            self.user_coords = SkyCoord(ra=ra, dec=dec)
        
        self.name = name.capitalize()

        #name = input('''Welcome to AstroLoreBot v1.0!\nGiven an astrophysical object of your choice, I output the nearest object on the sky referenced in sci-fi.\nWhenever you're ready, name your object:\n>>> ''')
        self.scifi_dataframe['ang_sep'] = SkyCoord(ra=self.scifi_dataframe.ra.values, dec=self.scifi_dataframe.dec.values).separation(self.user_coords).value
        close_object = self.scifi_dataframe.loc[self.scifi_dataframe.ang_sep.idxmin()]
        return close_object
    

    def output_lore(self, close_object:pd.Series):
        # Convert string to list of sources
        raw = close_object.scifi_source.strip("()")
        sources = [s.strip() for s in raw.split(",")]
        formatted_sources = self.format_sources(sources)

        # Threshold for "exact match"
        sep = round(close_object.ang_sep, 5)
        if sep < 0.01:
            output = (
                f"\nSearching around {self.name}...\n"
                f"Your chosen object is referenced in science fiction!\n"
                f"\nThe {close_object['name']} {close_object.object_type} appears/is referenced in {formatted_sources}. Here's some lore about {close_object['name']}:\n"
                f"\n{close_object.lore}\n"
            )
        else:
            output = (
                f"\nSearching around {self.name}...\n"
                f"The nearest object referenced in sci-fi is {sep} degrees away — "
                f"The {close_object['name']} {close_object.object_type}. "
                f"Here's some lore about {close_object['name']}:\n"
                f"\nThe {close_object['name']} {close_object.object_type} appears/is referenced in {formatted_sources}. {close_object.lore}"
            )

        return output

    def init_catalog_map(self, closest_object:pd.Series):
 
        # TODO: Simplify this function (if time)
        coords = SkyCoord(ra=self.scifi_dataframe.ra.values, dec=self.scifi_dataframe.dec.values)

        ra_rad = pd.DataFrame(np.radians(coords.ra.value))
        ra_rad = np.remainder(ra_rad + 2*np.pi, 2*np.pi)
        ra_rad[ra_rad > np.pi] -= 2*np.pi
        ra_rad = -ra_rad

        dec_rad = pd.DataFrame(np.radians(coords.dec.value))

        closest_coords = SkyCoord(ra=closest_object.ra, dec=closest_object.dec)
        closest_ra_rad, closest_dec_rad = self.convert_to_plotting_rad(closest_coords)

        return ra_rad, dec_rad, closest_ra_rad, closest_dec_rad

    def convert_to_plotting_rad(self, coords_in_deg):

        closest_ra_rad = np.radians(coords_in_deg.ra.value)
        closest_ra_rad = np.remainder(closest_ra_rad + 2*np.pi, 2*np.pi)
        closest_ra_rad -= 2 * np.pi if closest_ra_rad > np.pi else 0
        closest_ra_rad = -closest_ra_rad
        closest_dec_rad = np.radians(coords_in_deg.dec.value)
        return closest_ra_rad, closest_dec_rad

    def get_catalog_map(self, user_name=None):

        if user_name == None:
            user_name = 'Arcturus'

        user_coords = self.get_coords_from_name(user_name)
        user_ra_rad, user_dec_rad = self.convert_to_plotting_rad(user_coords)

        closest_object = self.find_closest_object(user_name)
        closest_name = self.name_of_object(closest_object)
        ra_rad, dec_rad, closest_ra_rad, closest_dec_rad = self.init_catalog_map(closest_object)

        fig, ax = plt.subplots(subplot_kw={'projection': 'aitoff'}, figsize=(26,9))

        fig.patch.set_facecolor('black')           # Background of the figure
        ax.set_facecolor('black')                  # Background of the plot area

        ax.scatter(ra_rad, dec_rad, c='white', marker='*', s=60)
        ax.scatter(closest_ra_rad, closest_dec_rad, c='gold', marker='*', s=300)
        ax.scatter(user_ra_rad, user_dec_rad, c="blue", marker="o", s=100)

        ra_hour_ticks_deg = np.arange(0, 360, 30)  # 0h to 23h
        ra_hour_ticks_rad = -np.radians(np.remainder(ra_hour_ticks_deg, 360))  # Negate!
        ra_hour_ticks_rad = np.remainder(ra_hour_ticks_rad + 2*np.pi, 2*np.pi)
        ra_hour_ticks_rad[ra_hour_ticks_rad > np.pi] -= 2*np.pi
        ra_hour_labels = [f'{int((deg / 15) % 24)}h' for deg in ra_hour_ticks_deg]
        ax.set_xticks(ra_hour_ticks_rad)
        ax.set_xticklabels(ra_hour_labels, fontsize=16, color='white')

        dec_ticks_rad = ax.get_yticks()
        dec_ticks_deg = np.degrees(dec_ticks_rad)
        dec_tick_labels = [f"{int(np.round(deg))}°" for deg in dec_ticks_deg]
        ax.set_yticks(dec_ticks_rad)
        ax.set_yticklabels(dec_tick_labels, color='white', fontsize=24)

        ax.spines['geo'].set_edgecolor('white')
        ax.spines['geo'].set_linewidth(1)

        ax.set_xlabel(r'$RA$', fontsize=24, color='white')
        ax.set_ylabel(r'$DEC$', fontsize=24, color='white')

        ax.xaxis.set_tick_params(labelsize=22, color='white')
        ax.yaxis.set_tick_params(labelsize=24, color='white')

        if closest_ra_rad != user_ra_rad and \
           closest_dec_rad != user_dec_rad:
            ax.annotate(
                '',                                      # No text
                xy=(closest_ra_rad, closest_dec_rad),  # Arrowhead (end) point
                xytext=(user_ra_rad, user_dec_rad),      # Start point
                arrowprops=dict(
                    arrowstyle='-|>',                    # Style: simple arrow
                    color='white',                       # Arrow color
                    lw=1,                                # Line width
                    linestyle='--',
                    shrinkA=10,
                    shrinkB=5
                ), zorder=-9999
            )

        # text for the closest object in the dataset
        ax.text(closest_ra_rad, closest_dec_rad-.06, 
                closest_name, ha='center', va='top', color='gold', 
                fontsize=14, bbox=dict(facecolor='gainsboro', alpha=0.5))
        # text for the object provided by the user
        ax.text(user_ra_rad, user_dec_rad-.06, 
                user_name, ha='center', va='top', color='white', 
                fontsize=14, bbox=dict(facecolor='gainsboro', alpha=.5))

        ax.grid(True, alpha=.6, color='white', linewidth=1)
        return fig, ax


    def load_aladin(self):
        """Launch Aladin window to observe nearest sci-fi source"""        
        if_vis = input('\nDo you want to observe the source in the real world?\n>>> ').strip().lower()
        if if_vis in ('yes', 'y'):
            coord_close_star = SkyCoord(ra=self.close_object.ra, dec=self.close_object.dec)
            url = f"https://aladin.u-strasbg.fr/AladinLite/?target={coord_close_star.ra.deg}%20{coord_close_star.dec.deg}&fov=1.5"
            webbrowser.open(url)




