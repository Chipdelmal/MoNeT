from collections import defaultdict
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import plotly.express as px
import matplotlib as mpl
import seaborn as sns
import networkx as nx
import pandas as pd
import numpy as np
import simulator
import detector

# Helpers

def get_label_counts(results, cluster_num, t=None, kernels=None):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        cluster_num : The cluster to use for counting labels
        t           : The time step to use for labels. If None, defaults to the time step used for experiments
        kernels     : A list of kernel names to get label counts for. These names must be in results[c].keys()
        
    Returns:
        The counts of bridges, sinks, and sources when `cluster_num` clusters are used.
        If any of the counts are zero, then they will NOT be omitted in the final result.
    """
    df = pd.DataFrame()
    names = results[cluster_num].keys() if kernels is None else kernels
    for name in names:
        s = results[cluster_num][name]
        counts = s.cdata(t).groupby('type').size().to_frame().rename(columns={0 : "count"})
        if 'bridge' not in counts.index:
            counts = counts.append(pd.DataFrame([0], index=['bridge'], columns=['count']))
        if 'sink'   not in counts.index:
            counts = counts.append(pd.DataFrame([0], index=['sink'], columns=['count']))
        if 'source' not in counts.index:
            counts = counts.append(pd.DataFrame([0], index=['source'], columns=['count']))
        counts = pd.concat({name : counts}, names=['name'])
        df = pd.concat([df, counts])
    df['clusters'] = cluster_num
    return df

def get_steps(s, k, start=None, final=None):
    """
    Input(s):
        s       : When `final` is None, use this simulator's `ss_step` as the final step
        k       : The number of evenly spaced values
        start   : The first time step to show in the plot
        final   : The last time step to show in the plot (should be greater than `start`)
        
    Returns:
        `k` evenly spaced integer values from `start` to `final` (inclusive). If `start`
        and `final` are not specified, then `start` defaults to 0 and `final` defaults to 
        the step at which steady state occurs. If `k` is not an integer, the function 
        returns `k`.
    """
    if not isinstance(k, int):
        return k
    
    if start is None: start = 0
    if final is None: final = s.ss_step
    
    if k == final - start + 1:
        return np.arange(start, final + 1)
    else:
        return np.round(np.linspace(start, final, k)).astype(int)

# Static Plots

def plot_avg_abs_change_in_population(results, kernels=None, k=200, start=None, final=None, fs=(8,8)):
    """
    Input(s):
        results    : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        kernels    : A list of kernel names to plot. These names must be in results[c].keys()
        k          : The number of evenly spaced values
        start      : The first time step to show in the plot
        final      : The last time step to show in the plot (should be greater than `start`)
        fs         : The figure size as a tuple of the form (width, height)
        
    Returns:
        A graph of the average absolute change in population over the specified interval. 
        The average absolute change in population is computed by first taking the absolute 
        difference in population between time steps t + 1 and t over all nodes and 
        computing the average of the resulting absolute differences. These values are 
        plotted against time over `k` evenly spaced values in the interval [`start`, 
        `final`]. A custom range may be used if `k` is passed in as a list of ints. To plot 
        only a specific set of kernels, pass a list of the kernel names as strings to the
        `kernels` parameter. By default all kernels in `results` are plotted.
    """
    # Steady state progression does not depend on clustering size,
    # so we can arbitrarily pick the first cluster for plotting
    cluster_num = list(results.keys())[0]
    df = pd.DataFrame()
    if final   is None: final   = np.max([s.ss_step for d in results[cluster_num].values()])
    if kernels is None: kernels = results[cluster_num]
    for n, s in results[cluster_num].items():
        if n in kernels:
            steps = get_steps(s, k, start, final)
            start = steps[0]
            final = steps[-1]
            popls = s.get_sizes(np.arange(start, final + 1))[:, steps]
            temp = pd.DataFrame()
            temp['means'] = np.mean(np.abs(np.diff(popls, axis=1)), axis=0)
            temp['kname'] = str(n)
            temp['steps'] = steps[1:]
            df = pd.concat([df, temp])
    plt.figure(figsize=fs)
    sns.lineplot(x="steps", y="means", hue="kname", data=df, legend='full', palette='muted')
    plt.title("Steady State Progression")
    plt.xlabel("Time Step")
    plt.ylabel("Mean Absolute Change in Population")
    
def label_counts_barplot(results, cluster_num, t=None, kernels=None, fs=(8,6)):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        cluster_num : The cluster to use for counting labels
        t           : The time step to use for labels. If None, defaults to the time step used for experiments
        kernels     : A list of kernel names to get label counts for. These names must be in results[c].keys()
        fs          : The figure size as a tuple of the form (width, height)
        
    Returns:
        A side by side bar plot of the sink/bridge/source counts for each kernel. To plot 
        only a specific set of kernels, pass a list of the kernel names as strings to the 
        `kernels` parameter.
    """
    df = get_label_counts(results, cluster_num, t, kernels).reset_index().rename(columns={'level_1' : 'type'})
    plt.figure(figsize=fs)
    sns.barplot(x="name", y="count", hue="type", data=df)
    plt.title(f"Sink/Bridge/Source Counts using {cluster_num} Cluster(s)")
    plt.xticks(rotation=60);
    
def label_proportions_barplot(results, cluster_num, t=None, kernels=None, fs=(8,6)):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        cluster_num : The cluster to use for counting labels
        t           : The time step to use for labels. If None, defaults to the time step used for experiments
        kernels     : A list of kernel names to get label counts for. These names must be in results[c].keys()
        fs          : The figure size as a tuple of the form (width, height)
        
    Returns:
        A side by side bar plot of the sink/bridge/source counts for each kernel. To plot 
        only a specific set of kernels, pass a list of the kernel names as strings to the 
        `kernels` parameter.
    """
    df = get_label_counts(results, cluster_num, t, kernels).reset_index().rename(columns={'level_1' : 'type'})
    df['count'] = df.groupby('name')['count'].apply(lambda x: x / sum(x))
    plt.figure(figsize=fs)
    sns.barplot(x="name", y="count", hue="type", data=df)
    plt.title(f"Sink/Bridge/Source Proportions using {cluster_num} Cluster(s)")
    plt.ylabel('proportion')
    plt.xticks(rotation=60);

def label_counts_lineplot(results, kernel_name, t=None, fs=(8,6)):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        kernel_name : The kernel to use for plotting as a string. This name must be in results[c].keys()
        t           : The time step to use for labels. If None, defaults to the time step used for experiments
        fs          : The figure size as a tuple of the form (width, height)
    
    Returns:
        A lineplot of sink/bridge/source count (at time step `t`) versus clusters for `kernel_name`.
        
    Notes:
        If `t` is not None, then the experiments will be rerun with the new value. Thus, it is recommended to only use
        `t` if the number of clusters used for experiments is small. If for whatever reason this function is to be called
        repeatedly with the same `t`, then it is much more efficient to pass in `t` on the first call and set `t` equal 
        to None for the rest of the calls.
    """
    df = pd.concat([get_label_counts(results, c, t, [kernel_name]) for c in results])\
           .reset_index()\
           .rename(columns={'level_1' : 'type'})
    plt.figure(figsize=fs)
    sns.lineplot(x="clusters", y="count", hue="type", data=df)
    plt.title(f"Sink/Bridge/Source Counts vs. Cluster(s) for {kernel_name}")
    plt.xticks(rotation=30);
    
def community_populations_barplot(results, cluster_num, kernel_name, plot_type='bar', t=None, fs=(8,6)):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        cluster_num : The cluster to use for counting labels
        kernel_name : The kernel to use for plotting as a string. This name must be in results[c].keys()
        plot_type   : Either 'bar' | 'barh'
        t           : The time step to extract population sizes from (default is steady state)
        fs          : The figure size as a tuple of the form (width, height)
    
    Returns:
        A plot of the population size of each community for `kernel_name` when 
        `cluster_num` clusters are used.
    """
    s = results[cluster_num][kernel_name]
    n = s.ndata()
    n['pop'] = s.migrate(s.ss_step if t is None else t)
    plt.figure(figsize=fs)
    n.groupby('cid')['pop'].sum().plot(kind=plot_type)
    plt.title(f"Distribution of Population Size per Community for {kernel_name}")
    plt.ylabel('Population Size')

def community_populations_lineplot(results, cluster_num, kernel_name, k=200, start=None, final=None, fs=(8,6)):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        cluster_num : The cluster to use for counting labels
        kernel_name : The kernel to use for plotting as a string. This name must be in results[c].keys()
        k           : The number of evenly spaced values
        start       : The first time step to show in the plot
        final       : The last time step to show in the plot (should be greater than `start`)
        fs          : The figure size as a tuple of the form (width, height)
    
    Returns:
        A lineplot of sink/bridge/source count versus clusters for `kernel_name`.
    """
    s = results[cluster_num][kernel_name]
    df = pd.DataFrame()
    copy = s.ndata()
    
    steps = get_steps(s, k, start, final)
    start = steps[0]
    final = steps[-1]
    populations = s.get_sizes(np.arange(start, final + 1))[:, steps]
    for i in range(populations.shape[1]):
        copy['pop'] = populations[:, i]
        temp = copy[['cid', 'pop']].groupby('cid').sum()
        temp['step'] = i
        df = pd.concat([df, temp])
        
    df = df.reset_index()
    plt.figure(figsize=fs)
    sns.lineplot(x="step", y="pop", hue="cid", data=df, legend='full', palette='muted')
    plt.title(f"Community Population Size vs. Time for {kernel_name}")
    plt.xlabel('Time Step')
    plt.ylabel('Population Size')
    plt.xticks(rotation=30);
    
def community_nodes_barplot(results, cluster_num, kernel_name, fs=(8,6)):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        cluster_num : The cluster to use for counting labels
        kernel_name : The kernel to use for plotting as a string. This name must be in results[c].keys()
        fs          : The figure size as a tuple of the form (width, height)
        
    Returns:
        A plot of the number of nodes in each community for `kernel_name` when
        `cluster_num` clusters are used.
    """
    plt.figure(figsize=fs)
    results[cluster_num][kernel_name].ndata().groupby('cid').size().plot(kind='bar');
    plt.title(f"Distribution of Number Nodes per Community for {kernel_name}")
    plt.ylabel('Number of Nodes')
    
def community_proportions_barplot(results, cluster_num, kernel_name, t=None, fs=(8,6)):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        cluster_num : The cluster to use for counting labels
        kernel_name : The kernel to use for plotting as a string. This name must be in results[c].keys()
        t           : The time step to extract population sizes from (default is steady state)
        fs          : The figure size as a tuple of the form (width, height)
        
    Returns:
        The proportion of the total population and the proportion of the total number of 
        nodes in each community as a side by side bar plot.
    """
    s = results[cluster_num][kernel_name]
    c = s.ndata()
    c['pop'] = s.migrate(s.ss_step if t is None else t)
    h = len(c['cid'].unique())
    nds = pd.DataFrame({
        'y'   : c.groupby('cid').size() / c.shape[0],
        'hue' : ['nodes'] * h
    })
    pop = pd.DataFrame({
        'y'   : c.groupby('cid')['pop'].sum() / c['pop'].sum(),
        'hue' : ['population'] * h
    })
    df = pd.concat([nds, pop]).reset_index()
    plt.figure(figsize=fs)
    sns.barplot(x='cid', y='y', hue='hue', data=df)
    plt.title(f'Population and Node Proportions by Community for {kernel_name}')
    plt.xlabel('Community ID')
    plt.ylabel('Proportion');
    
# Interactive Plots
    
def plot_interactive_label_counts(results, kernel_name, t=None):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        kernel_name : The kernel to use for plotting as a string. This name must be in results[c].keys()
        t           : The time step to use for labels. If None, defaults to the time step used for experiments
    
    Returns:
        A side by side bar plot of the sink/bridge/source counts (at time step `t`) for `kernel_name` over all 
        clusters.
    """
    df = pd.concat([get_label_counts(results, c, t, [kernel_name]) for c in results])\
           .reset_index()\
           .rename(columns={'level_1' : 'type'})
    fig = px.bar(df, x="type", y="count", color="type",
      animation_frame="clusters", animation_group="clusters", range_y=[0, df["count"].max()])
    fig.show()
    
def plot_population_distribution(results, kernel_name, cluster_num=None, k=200, start=None, final=None):
    """
    Input(s):
        results     : A nested dictionary such that results[c][k] is the simulator for kernel k using c clusters
        kernel_name : The kernel to use for plotting as a string. This name must be in results[c].keys()
        cluster_num : The cluster to use for goloring nodes
        k           : The number of evenly spaced values
        start       : The first time step to show in the plot
        final       : The last time step to show in the plot (should be greater than `start`)
    
    Returns:
        An interactive visualization of the population for every state from time step 
        `start` to time step `final` (inclusive) over `k` values for `kernel_name`. A 
        custom range may be used if `k` is passed in as a list of ints.
    """
    s, c = None, None
    if cluster_num is None:
        # Steady state progression does not depend on clustering size,
        # so we can arbitrarily pick the first cluster for plotting
        s = results[list(results.keys())[0]][kernel_name]
        c = "node"
    else:
        # If a cluster_num is specified, each node will be colored 
        # according to its community
        s = results[cluster_num][kernel_name]
        c = "cid"
    
    steps = get_steps(s, k, start, final)
    start = steps[0]
    final = steps[-1]
    popls = s.get_sizes(np.arange(start, final + 1)).T[steps]
    df = pd.DataFrame({
        'node'       : list(range(len(s.tmtx))) * len(popls),
        'population' : popls.flatten(),
        'step'       : np.array([[i] * len(s.tmtx) for i in steps]).flatten(),
        'cid'        : list(s.ndata()['cid']) * len(popls)
    })
    
    fig = px.bar(df, x="node", y="population", color=c, title=f"Population Distribution for {kernel_name}",
      animation_frame="step", animation_group="node", range_y=[0, df['population'].max()])
    
    fig.show()
    
# Network Plot Functions

def get_discrete_colorscale(cmap, num_categories, shuffle=False, seed=None):
    """
    Inputs:
        cmap           : a matplotlib colormap object
        num_categories : the number of categorical variables
        shuffle        : whether or not to shuffle the colors for each category
        seed           : seed for shuffling
        
    Returns:
        A colorscale consistent with plotly's go.Scatter colorscale parameter.
    """
    colorscale = []
    c_order = (1 / num_categories) * np.arange(num_categories + 1)
    c_order_shuffled = c_order.copy()
    
    # Shuffling allows us to get different segments of a qualitative colormap
    if shuffle:
        if seed is not None:
            rng = np.random.RandomState(seed)
            rng.shuffle(c_order_shuffled)
        else:
            np.random.shuffle(c_order_shuffled)
    
    # Creates boundaries for the discrete colorscale
    for i in range(1, num_categories + 1):
        rgb = list(map(np.uint8, np.array(cmap(c_order_shuffled[i])[:3])*255))
        colorscale.append([c_order[i - 1], 'rgb'+str((rgb[0], rgb[1], rgb[2]))])
        colorscale.append([c_order[i    ], 'rgb'+str((rgb[0], rgb[1], rgb[2]))])
    return colorscale

def get_edge_traces(G, locs, edge_colorsdict, edge_prec):
    """
    Input(s):
        G               : the network as a networkx graph
        locs            : the result of detector.run().ndata()
        edge_colorsdict : a dictionary such that each key is an rgb tuple and the corresponding value is a list
                          of edges that should be colored according to the rgb value in the key.
        edge_prec       : the precision to use when displaying edge weights
        
    Returns:
        The edge traces for plotting the network.
    """
    edge_traces = []
    for color, edges in edge_colorsdict.items():
        text_x, text_y, ewghts = [], [], []
        for u, v, tw, sw in edges:
            x0, y0 = G.nodes[u]['pos']
            x1, y1 = G.nodes[v]['pos']
            text_x.append((x0+x1)/2)
            text_y.append((y0+y1)/2)
            ewghts.append('true weight: {}<br>scaled weight: {}'.format(round(tw, edge_prec), round(sw, edge_prec)))
            line_type = 'dot' if locs.loc[u, 'cid'] != locs.loc[v, 'cid'] else 'solid'
            edge_traces.append(
                go.Scatter(
                    x=[x0, x1], y=[y0, y1],
                    line=dict(
                        dash=line_type,
                        width=sw,
                        color=f'rgb{color}'),
                    mode='lines'
                )
            )

        wght_trace = go.Scatter(
            x=text_x,y=text_y,
            mode='markers',
            marker_size=0.5,
            text=ewghts,
            textposition='top center',
            hovertemplate='%{text}<extra></extra>',
            marker=dict(color=f'rgb{color}')
        )
        edge_traces.append(wght_trace)
        
    return edge_traces

def get_brdr_traces(G, locs, brdr_colorscale, bordr_fn, bordr_cb, bcbx):
    """
    Input(s):
        G               : the network as a networkx graph
        locs            : the result of detector.run().ndata()
        brdr_colorscale : a colorscale consistent with plotly. See: https://plotly.com/python/colorscales/
        bordr_fn        : a function that takes in the scaled node sizes as a pandas series and scales them in some way
        
    Returns:
        The border traces for plotting the network.
    """
    sizes = bordr_fn(locs['size'])
    codes = { t : i for i, t in enumerate(sorted(locs['ctype'].unique())) }
    return go.Scatter(
        x=locs['lon'], y=locs['lat'],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=bordr_cb,
            colorscale=brdr_colorscale,
            color=locs['ctype'].map(codes),
            size=sizes[0] if len(set(sizes)) == 1 else sizes,
            colorbar=dict(
                thickness=15,
                title='Community Type',
                xanchor='left',
                titleside='right',
                ticktext=list(codes.keys()),
                tickvals=list(codes.values()),
                x=bcbx
            ),
            line_width=0))

def get_node_traces(G, locs, node_colorscale, node_prec, nodes_cb, ncbx, n_offset):
    """
    Input(s):
        G               : the network as a networkx graph
        locs            : the result of detector.run().ndata()
        node_colorscale : a colorscale consistent with plotly. See: https://plotly.com/python/colorscales/
        node_prec       : the precision to use when displaying node populations
        
    Returns:
        The node traces for plotting the network.
    """
    node_t = []
    for n in G.nodes():
        cid, nid = locs.loc[n, "cid"], locs.loc[n, "index"]
        typ, pop = locs.loc[n, "ctype"], round(locs.loc[n, "pop"], node_prec)
        node_t.append(f'cid: {cid}<br>nid: {nid}<br>ctype: {typ}<br>pop: {pop}')
        
    ticks = locs['color'].unique()
    ticks = ticks - (ticks / len(ticks)) + n_offset
    sizes = locs['size']
    return go.Scatter(
        x=locs['lon'], y=locs['lat'],
        mode='markers',
        hoverinfo='text',
        text=node_t,
        marker=dict(
            showscale=nodes_cb,
            colorscale=node_colorscale,
            reversescale=True,
            color=locs['color'],
            size=sizes[0] if len(set(sizes)) == 1 else sizes,
            colorbar=dict(
                thickness=15,
                title='Community Color',
                xanchor='left',
                titleside='right',
                ticktext=locs['cid'].unique(),
                tickvals=ticks,
                x=ncbx
            ),
            line_width=0))

def get_colorbar_positions(bordr_cb, edges_cb, nodes_cb, positions):
    assert len(positions) <= 3, "Too many coordinates specified"
    assert len(positions) == sum(map(bool, [bordr_cb, edges_cb, nodes_cb])), "Incorrect number of coordinates received"
    positions = np.array(([float('inf')] * (3 - len(positions))) + positions)
    minx, midx, maxx = positions[np.argsort(positions)]
    if not bordr_cb and not edges_cb and not nodes_cb: return (0   , 0   , 0   )
    if not bordr_cb and not edges_cb and     nodes_cb: return (0   , 0   , minx)
    if not bordr_cb and     edges_cb and not nodes_cb: return (0   , minx, 0   )
    if not bordr_cb and     edges_cb and     nodes_cb: return (0   , midx, minx)
    if     bordr_cb and not edges_cb and not nodes_cb: return (minx,    0, 0   )
    if     bordr_cb and not edges_cb and     nodes_cb: return (midx,    0, minx)
    if     bordr_cb and     edges_cb and not nodes_cb: return (midx, minx, 0   )
    if     bordr_cb and     edges_cb and     nodes_cb: return (maxx, midx, minx)

def extract_geo_coords(geo_data):
    pts = []
    for feature in geo_data:
        if feature['geometry']['type'] == 'Polygon':
            pts.extend(feature['geometry']['coordinates'][0])    
            pts.append([None, None])
        elif feature['geometry']['type'] == 'MultiPolygon':
            for polyg in feature['geometry']['coordinates']:
                pts.extend(polyg[0])
                pts.append([None, None])
        elif feature['geometry']['type'] == 'LineString': 
            points.extend(feature['geometry']['coordinates'])
            points.append([None, None])
        else:
            pass # Don't need geometry type for plotting the map
    x, y = zip(*pts)
    return x, y

def plot_network(tmtx, locs,
                 nodes_cm=cmx.get_cmap('cool')   , nodes_cb=False, nodes_fn=lambda n: [4.0] * len(n),
                 edges_cm=cmx.get_cmap('Purples'), edges_cb=False, edges_fn=lambda w: [0.5] * len(w),
                 bordr_cm=cmx.get_cmap('gray')   , bordr_cb=False, bordr_fn=lambda b: [7.0] * len(b),
                 min_popl=0, min_prob=0, max_prob=1,  
                 nodes_pr=1, edges_pr=5,
                 n_offset=0.4, cb_xlocs=[],
                 shufflec=False, rng_seed=None, 
                 geo_data=None, geo_wdth=1.5, geocolor='#999999',
                 paper_bg="LightSteelBlue", netwk_bg=None,
                 fig_wdth=None, fig_hght=None):
    """
    Input(s):
        tmtx     : the state transition matrix corresponding to `locs`
        locs     : the result of detector.run().ndata()
        nodes_cm : a matplotlib colormap object to be used for coloring nodes
        nodes_cb : if True, shows the colorbar for the community IDs. The location must be specified using `cb_xlocs`
        nodes_fn : a function that takes in all node populations as a pandas series and scales them in some way
        min_popl : if a node's population is very small use this as its population instead
        nodes_pr : the precision to use when displaying node populations
        edges_cm : a matplotlib colormap object to be used for coloring edges
        edges_fn : a function that takes in all edge weights as a pandas series and scales them in some way
        edges_cb : if True, shows the colorbar for the edge weights. The location must be specified using `cb_xlocs`
        min_prob : draw an edge if its weight is greater than or equal to this value
        max_prob : draw an edge if its weight is less than or equal to this value
        edges_pr : the precision to use when displaying edge weights
        bordr_cm : a matplotlib colormap object to be used for coloring node borders
        bordr_fn : a function that takes in the scaled node sizes as a pandas series and scales them in some way
        bordr_cb : if True, shows the colorbar for the node borders. The location must be specified using `cb_xlocs`
        n_offset : adjusts the vertical positions of the cid labels on the nodes colorbar
        cb_xlocs : a list consisting of x locations for the colorbars. For readability purposes, the colorbars will
                   be arranged in the order: nodes, edges, borders. The number of coordinates must match the number 
                   of colobars to plot. If not, an error will be raised.
        shufflec : if True, borders can have colors from different segments of its colormap instead of just the lower/middle/upper segments
        rng_seed : seed to be used for shuffling. Only has an effect if `shufflec` is True
        geo_data : a list containing geojson.feaature.Feature objects for plotting the background
        geo_wdth : line width of the map border
        geocolor : color of the map border
        paper_bg : the background color of the paper where the graph is drawn
        netwk_bg : the background color of the plotting area in between the x and y axes 
        fig_wdth : the width of the resulting figure
        fig_hght : the height of the resulting figure
        
    Returns:
        An interactive plot of the sinks/sources/bridges in the given network. 
    
    Notes:
        - By default:
            - all edges are the same thickness, all nodes are the same size, and all borders are the same size
            - all edges are included and no populations are rescaled
        - If any of `nodes_fn`, `edges_fn`, or `bordr_fn` return negative values, results are undefined
        - Filtering occurs on the original data first, then functions are applied to the remaining data
    """
    # Ensures node numberings are consistent with transition matrix numberings
    ndata = locs.copy().reset_index()
    
    # Removes self transitions
    np.fill_diagonal(tmtx, 0)
    
    # Ensures all population sizes are greater than or equal to min_popl
    ndata['pop'] = ndata['pop'].apply(lambda p: max(p, min_popl))                 
    
    # Converts data to networkx graph and filters out edges with weights below `min_prob`
    G = nx.Graph()
    G = nx.from_numpy_matrix(tmtx)
    G.add_nodes_from([ (i, {'pos' : (r['lon'], r['lat'])}) for i, r in ndata.iterrows() ])
    G.remove_edges_from([(n1, n2) for n1, n2, w in G.edges.data('weight') if w < min_prob or w > max_prob])
    
    # This helps with colorbar formatting
    unique_cids = ndata['cid'].unique()
    bcbx, ecbx, ncbx= get_colorbar_positions(bordr_cb, edges_cb, nodes_cb, cb_xlocs)
    ndata['color'] = ndata['cid'].map({cid : i for i, cid in enumerate(sorted(unique_cids))})
    
    # Apply scaling functions to nodes
    ndata['size'] = nodes_fn(ndata['pop'])
    
    # Apply scaling and styling to edges (if any), then get edge traces + edge colorbar trace
    if len(G.edges) != 0:
        new_weights = edges_fn(np.array(list(map(lambda t: t[2]['weight'], G.edges(data=True)))))
        nx.set_edge_attributes(G, {(u, v) : {'scaled' : sw} for (u, v), sw in zip(G.edges, new_weights)})
        edge_colorsdict = defaultdict(list)
        min_weight, max_weight = np.min(new_weights), np.max(new_weights)
        for u, v, d in G.edges(data=True):
            normalized = mpl.colors.Normalize(vmin=min_weight, vmax=max_weight)
            scalar_map = cmx.ScalarMappable(norm=normalized, cmap=edges_cm)
            edge_colorsdict[tuple(np.array(scalar_map.to_rgba(d['scaled']))*255)].append((u, v, d['weight'], d['scaled']))
        edge_traces = get_edge_traces(G, ndata, edge_colorsdict, edges_pr)
        ebar_trace = [go.Scatter(x=[None], y=[None],
                                 mode='markers',
                                 marker=dict(
                                     colorscale=get_discrete_colorscale(edges_cm, 255, shuffle=False), 
                                     showscale=edges_cb,
                                     cmin=min_weight,
                                     cmax=max_weight,
                                     colorbar=dict(
                                         thickness=15,
                                         title='Scaled Edge Weight',
                                         xanchor='left',
                                         titleside='right',
                                         x=ecbx)
                                 ),
                                 hoverinfo='none')]
    else:
        edge_traces = []
        ebar_trace  = []
    
    # Set styling for nodes and borders
    brdr_colorscale = get_discrete_colorscale(bordr_cm, len(ndata['ctype'].unique()), shuffle=shufflec, seed=rng_seed)
    node_colorscale = get_discrete_colorscale(nodes_cm, len(unique_cids)            , shuffle=False   , seed=None)
    
    # Retrieve traces for plotly
    brdr_traces = get_brdr_traces(G, ndata, brdr_colorscale, bordr_fn, bordr_cb, bcbx)
    node_traces = get_node_traces(G, ndata, node_colorscale, nodes_pr, nodes_cb, ncbx, n_offset)
    
    # Add map border if specified
    map_trace = []
    if geo_data is not None:
        x, y = extract_geo_coords(geo_data)
        map_trace.append(go.Scatter(x=x, y=y, 
                                    mode='lines', 
                                    line_color=geocolor, 
                                    line_width=geo_wdth,
                                    hoverinfo='skip'))
    
    # Plot data
    fig = go.Figure(data=map_trace + edge_traces + ebar_trace + [brdr_traces, node_traces],
                layout=go.Layout(
                    width=fig_wdth,
                    height=fig_hght,
                    paper_bgcolor=paper_bg,
                    plot_bgcolor=netwk_bg,
                    title='<br><b>Sink/Source/Bridge Network</b>',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=55),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
               )
    
    fig.show()