import pandas as pd
from astropy.coordinates import SkyCoord

name = input('''Welcome to AstroLoreBotv1.0!\nGiven an astrophysical object of your choice, I output the nearest object on the sky referenced in sci-fi\nWhenever you're ready name your object\n>>>''')
coords = SkyCoord.from_name(name)
name = name.capitalize()

df = pd.read_csv('scifi_dataset.csv')

df['ang_sep'] = SkyCoord(ra=df.ra.values, dec=df.dec.values).separation(coords).value

close_star = df.loc[df.ang_sep.idxmin()]

output = (
    f"Wow, {name}!\n"
    f"The nearest object referenced in sci-fi is {round(close_star.ang_sep, 5)} degrees away, "
    f"the {close_star['name']} {close_star.object_type}.\n"
    f"Here's some lore about {close_star['name']}:\n"
    f"{close_star.lore}"
)

print(output)