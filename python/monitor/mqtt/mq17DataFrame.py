import pandas as pd
import numpy  as np

from datetime import datetime, timedelta
from scipy    import interpolate

class mqDataFrame:
  def __init__(self, max_duration):
    # save initial parameter
    self.max_duration = max_duration

    self.timeframe = pd.DataFrame({
      "time": [], "ftime": [], "temp": [] })
    self.df_smooth = pd.DataFrame({
      "time": [], "temp": [] })

  def build_df_smooth(self):
    df_t = self.timeframe['ftime']   
    tck = interpolate.splrep(
        df_t, self.timeframe['temp'], s=0)

    idx = self.timeframe.index
    fst = df_t[idx[0]]
    lst = df_t[idx[-1]]

    xfit = np.arange(fst, lst, 0.1)
    yfit = interpolate.splev(xfit, tck, der=0)
    tfit = [datetime.fromtimestamp(f) for f in xfit]

    self.df_smooth = pd.DataFrame({
      "time": tfit,
      "temp": yfit
    })

  def remove_old(self, index, new_time):
    # remove old data
    obsolete = new_time \
      - timedelta(seconds=self.max_duration)

    self.timeframe = self.timeframe\
      [self.timeframe.time >= obsolete]

  def update_data(self, index, new_num, new_time):
    new_time_as_float = datetime.\
      timestamp(new_time)

    new_pair = pd.DataFrame({
      "time" : new_time,
      "ftime": new_time_as_float,
      "temp" : new_num
    }, index=[index])

    self.timeframe = pd.concat(
      [self.timeframe, new_pair])

  def get_timeframe(self):
    return self.timeframe

  def get_df_smooth(self):
    return self.df_smooth