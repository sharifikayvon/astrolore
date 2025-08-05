import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
import webbrowser

# User input
name = input('''Welcome to AstroLoreBot v1.0!\nGiven an astrophysical object of your choice, I output the nearest object on the sky referenced in sci-fi.\nWhenever you're ready, name your object:\n>>> ''')
coords = SkyCoord.from_name(name)
name = name.capitalize()

# Load data and compute angular separation
df = pd.read_csv('scifi_dataset.csv')
df['ang_sep'] = SkyCoord(ra=df.ra.values, dec=df.dec.values).separation(coords).value
close_star = df.loc[df.ang_sep.idxmin()]

# Format the sources cleanly
def format_sources(sources):
    if not sources:
        return ""
    elif len(sources) == 1:
        return sources[0]
    elif len(sources) == 2:
        return f"{sources[0]} and {sources[1]}"
    else:
        return f"{', '.join(sources[:-1])}, and {sources[-1]}"

# Convert string to list of sources
raw = close_star.scifi_source.strip("()")
sources = [s.strip() for s in raw.split(",")]
formatted_sources = format_sources(sources)

# Threshold for "exact match"
sep = round(close_star.ang_sep, 5)
if sep < 0.01:
    output = (
        f"\nWow, {name}! "
        f"Your chosen object is itself referenced in science fiction!\n"
        f"\nThe {close_star['name']} {close_star.object_type} appears/is referenced in {formatted_sources}. Here's some lore about {close_star['name']}:\n"
        f"\n{close_star.lore}\n"
    )
else:
    output = (
        f"\nWow, {name}! "
        f"The nearest object referenced in sci-fi is {sep} degrees away — "
        f"The {close_star['name']} {close_star.object_type}. "
        f"Here's some lore about {close_star['name']}:\n"
        f"\nThe {close_star['name']} {close_star.object_type} appears/is referenced in {formatted_sources}. {close_star.lore}"
    )

print(output)

# Ask for visualization
if_vis = input('\nDo you want to observe the source in the real world?\n>>> ').strip().lower()
if if_vis in ('yes', 'y'):
    coord_close_star = SkyCoord(ra=close_star.ra, dec=close_star.dec)
    url = f"https://aladin.u-strasbg.fr/AladinLite/?target={coord_close_star.ra.deg}%20{coord_close_star.dec.deg}&fov=1.5"
    webbrowser.open(url)
