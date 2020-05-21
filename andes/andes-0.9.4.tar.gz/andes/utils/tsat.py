import pandas as pd


def tsat_to_df(file):
    """
    Convert a TSAT XLS export to DataFrame
    """
    wb = pd.read_excel(file)

    df = wb.loc[6:]
    df.transpose()
    df.columns = ['Time', *range(len(wb.columns) - 1)]
    return df


def plot_comparison(system, variable, df, a, ylabel, tsat_header=('TSAT',), scale=1,
                    a_tsat=None,
                    left=None, right=None, legend=True):
    """
    Plot and compare ANDES and TSAT results
    """
    plot = system.TDS.plotter.plot
    plot_data = system.TDS.plotter.plot_data
    a_tsat = a if a_tsat is None else a_tsat

    fig, ax = plot(variable,
                   a=a,
                   ycalc=lambda x: scale * x,
                   ylabel=ylabel,
                   show=False,
                   line_styles=['-', '-.'],
                   left=left,
                   right=right,
                   legend=legend,
                   )

    fig, ax = plot_data(df['Time'].to_numpy(),
                        df[a_tsat].to_numpy(),
                        xheader=['Time [s]'],
                        yheader=[tsat_header[i] for i in a_tsat] if tsat_header is not None else None,
                        fig=fig,
                        ax=ax,
                        line_styles=['--', ':'],
                        left=left,
                        right=right,
                        legend=legend,
                        )
    return fig, ax
