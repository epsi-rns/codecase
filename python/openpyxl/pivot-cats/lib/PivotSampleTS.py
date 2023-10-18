from lib.PivotSample import PivotSample

class PivotSampleTS(PivotSample):
  def build_pivot(self) -> None:
    try:
      # Perform pivot operations
      df_pivot = self.df_table.pivot_table(
        index='Date', columns='Category',
        aggfunc='count', fill_value=0)

      # Sort the index by both month and day
      df_pivot.index = df_pivot. \
        index.to_series().apply(lambda x: x.date())
      df_pivot = df_pivot.sort_index()

      # Ensure all specified columns are present
      for cat in self.categories:
        if ('Number', cat) not in df_pivot.columns:
          df_pivot[('Number', cat)] = 0

      # Sort the columns (fruits) in alphabetical order
      self.df_pivot = df_pivot.sort_index(axis=1)

    except Exception as e:
      print("An error occurred " \
        + f"while processing data: {e}")

