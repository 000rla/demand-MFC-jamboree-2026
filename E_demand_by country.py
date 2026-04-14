import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from matplotlib.colors import Normalize

def main():
    dataset = pd.read_parquet("dataset/renewables-dataset.parquet")
    dataset["Time"] = pd.to_datetime(dataset["Time"])
    countries=[country for country in dataset["country"].unique()]

    for c in countries:
        dataset_c=dataset.iloc[np.where(dataset['country']==c)].copy() 
        IDs=[id for id in dataset_c["ID"].unique()]
        unique_lats=[lat for lat in dataset_c["latitude"].unique()]
        unique_lons=[lon for lon in dataset_c["longitude"].unique()]

        averages=dataset_c.groupby('ID')['demand_MWh'].mean()

        fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': ccrs.PlateCarree()})
        cmap=plt.cm.cividis
        norm = Normalize(vmin=min(averages), vmax=max(averages))
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

        ax.coastlines(resolution='50m')
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.BORDERS)

        ax.scatter(unique_lons,unique_lats,c=averages)
        plt.colorbar(mappable=sm, ax=ax, label='Demand in MWh')

        plt.title('Energy demand in '+c)

        plt.savefig('energy_demand_'+c+'.jpg')
        plt.show()

main()