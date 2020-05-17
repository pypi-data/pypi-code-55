from rohan.global_imports import *
from rohan.dandage.io_dict import read_dict,to_dict

def plot_peaks(df1):
    plt.figure(figsize=[60*(len(df1)//10000),3])
    ax=plt.subplot()
    df1.plot(x='time (ms)',y='db (log-scale) mean',ax=ax,legend=None)
    df1.plot.scatter(x='time (ms)',y='db (log-scale) mean peak',ax=ax,color='b')
    # df1.plot.scatter(x='time (ms)',y='db (log-scale) mean peak delay',ax=ax,color='g')
    ymax=ax.get_ylim()[1]
    def annot_rally(ax,x,y):
        ax.plot([x[('time (ms)', 'amin')],x[('time (ms)', 'amax')]],[y,y],color='lime')
        ax.text(np.mean([x[('time (ms)', 'amin')],x[('time (ms)', 'amax')]]),y,f"#{int(x.name)}",ha='center',va='bottom')
    _=df1.loc[~df1['db (log-scale) mean peak'].isnull(),:].groupby('rally #').agg({'time (ms)':[np.min,np.max,]}).apply(lambda x: annot_rally(ax,x,ymax),axis=1)
    # ax.legend(bbox_to_anchor=[1,1.2],loc='upper right')
    # ax.get_legend().remove()
    ymin,ymax=ax.get_ylim()
    _=ax.set_ylim(ymin,ymin+(ymax-ymin)*1.1)
    return ax
        
def plot_stats(dplot):
    # dplot=dplot.sort_values(by=['date'])
    # dplot['day #']=dplot['date'].rank()
    colxs=['rally #','day #']
    colys=['rally speed','rally duration','loudness (db)']
    from rohan.dandage.plot.colors import get_ncolors
    for c in colxs:
        dplot[c]=dplot[c].apply(int)
    for c in colxs[1:]:
        elements=[int(i) for i in sorted(dplot[c].unique())]
        element2color=dict(zip(elements,get_ncolors(len(elements),cmap='Reds')))
        # break
    legend2color={('day1' if ki==0 else 'latest') :element2color[k] for ki,k in enumerate([np.min(list(element2color.keys())),np.max(list(element2color.keys()))])}
    from rohan.dandage.plot.ax_ import set_legend_lines
    def plot_regplot(ax,dplot,colx,coly,line_color='r'):
        sns.regplot(x=colx, y=coly, data=dplot,lowess=True,
                scatter_kws={"color":"gray",'alpha':0.5},line_kws={"color":line_color},
                ax=ax)
        return ax
    lim_quantile=0.05
    fig,axs=plt.subplots(ncols=3,nrows=2,figsize=[12,8])
    for ax,(colx,coly) in zip(np.ravel(axs),itertools.product(colxs,colys)):
        if colx=='rally #':
            dplot.groupby([colxs[abs(colxs.index(colx)-1)]]).apply(lambda df: plot_regplot(ax,df,colx,coly,line_color=element2color[df.name]))
            set_legend_lines(ax,legend2color,param='color',params_legend={'frameon':True})
        else:
            plot_regplot(ax,dplot,colx,coly,line_color='r')
        ax.set_ylim(dplot[coly].quantile(lim_quantile),dplot[coly].quantile(1-lim_quantile))
        ax.ticklabel_format(style='plain',axis='x')
    plt.tight_layout()
    
    
def plot_stats_(cfg,dstatsp):
    # from ppong.plots import plot_stats
    from rohan.dandage.io_strs import get_datetime
    outp=f'plot/scatters_stats {get_datetime()}.png'
    plot_stats(read_table(dstatsp))
    savefig(outp)
    
def get02_plot_peaks(cfg,plot_peaksp):
    from ppong.plots import plot_peaks
    dn2dp=read_dict(cfg['date2dpeakp'])
    for k in dn2dp:
        outp=f'plot/line_time_db (log-scale) mean peak {k}.png'
        if not exists(outp):
            df1=read_table(f'data_analysed/data02_peaks/{k}.pqt')
            ax=plot_peaks(df1)
            savefig(outp,dpi=90)