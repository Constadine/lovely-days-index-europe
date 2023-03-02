def change_to_datetime(*dss):
    """
    Parameters
    ----------
    *dss : xarray.Dataset
        Converts time variable to Datetime64 type.

    Returns
    -------
    None.
    """
    for ds in dss:
        datetimeindex = ds.indexes['time'].to_datetimeindex()
        ds['time'] = datetimeindex
        
def select_time_period(*dss):
    pass