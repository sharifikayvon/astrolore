import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
import webbrowser
import os

class AstroLore():

    def __init__(self):
        path = os.path.dirname(__file__)
        self.scifi_dataframe = pd.read_csv(os.path.join(path, "data", "scifi_dataset.csv"))
        
        
    @staticmethod
    def format_sources(sources):
        """
        Formats output of sci-fi sources
        e.g. instead of 'Star Trek, Star Wars, Dune', output 'Star Trek, Star Wars, and Dune'

        Args:
            sources (string): string of sci-fi sources, e.g. '(Star Trek, Star Wars, Dune)'

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

    
    def closest_star_finder(self, name = None, coords=None):
        """
        Given either an input identifier, e.g. Arcturus, or coordinates (RA, DEC), this function searches the scifi_dataset 
        for the sci-fi source with the smallest angular separation

        Args:
            name (string, optional): . Defaults to None.
            coords (tuple, optional): tuple of RA+DEC strings in format ('00h00m00s', '00d00m00s'). Defaults to None.

        Returns:
            string: message to user describing nearest sci-fi star in dataset
        """        
        
        if name is None:
            name = 'Andromeda'
        if coords is None:
            self.coords = SkyCoord.from_name(name)
        else:
            ra, dec = coords
            self.coords = SkyCoord(ra=ra, dec=dec)
        
        self.name = name.capitalize()

        #name = input('''Welcome to AstroLoreBot v1.0!\nGiven an astrophysical object of your choice, I output the nearest object on the sky referenced in sci-fi.\nWhenever you're ready, name your object:\n>>> ''')
        self.scifi_dataframe['ang_sep'] = SkyCoord(ra=self.scifi_dataframe.ra.values, dec=self.scifi_dataframe.dec.values).separation(self.coords).value
        self.close_star = self.scifi_dataframe.loc[self.scifi_dataframe.ang_sep.idxmin()]


        # Convert string to list of sources
        raw = self.close_star.scifi_source.strip("()")
        sources = [s.strip() for s in raw.split(",")]
        formatted_sources = self.format_sources(sources)

        # Threshold for "exact match"
        sep = round(self.close_star.ang_sep, 5)
        if sep < 0.01:
            output = (
                f"\nWow, {self.name}! "
                f"Your chosen object is itself referenced in science fiction!\n"
                f"\nThe {self.close_star['name']} {self.close_star.object_type} appears/is referenced in {formatted_sources}. Here's some lore about {self.close_star['name']}:\n"
                f"\n{self.close_star.lore}\n"
            )
        else:
            output = (
                f"\nWow, {self.name}! "
                f"The nearest object referenced in sci-fi is {sep} degrees away — "
                f"The {self.close_star['name']} {self.close_star.object_type}. "
                f"Here's some lore about {self.close_star['name']}:\n"
                f"\nThe {self.close_star['name']} {self.close_star.object_type} appears/is referenced in {formatted_sources}. {self.close_star.lore}"
            )

        return output
    

    def visualize(self):
        """
        Launch Aladin window to observe nearest sci-fi source

        """        
        # Ask for visualization
        if_vis = input('\nDo you want to observe the source in the real world?\n>>> ').strip().lower()
        if if_vis in ('yes', 'y'):
            coord_close_star = SkyCoord(ra=self.close_star.ra, dec=self.close_star.dec)
            url = f"https://aladin.u-strasbg.fr/AladinLite/?target={coord_close_star.ra.deg}%20{coord_close_star.dec.deg}&fov=1.5"
            webbrowser.open(url)




