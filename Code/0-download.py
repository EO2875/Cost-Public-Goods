
import os

from utils import download_db_data, data_dir

download_db_data('SP.URB.TOTL.IN.ZS', os.path.join(data_dir, 'WB_UrbanPopPer.csv'))

