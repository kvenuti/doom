
import matplotlib.pyplot as plt
from statistics import mean, median
from rap_clean import verse
import re
import plotly.offline as offline
import plotly.figure_factory as ff
import plotly.graph_objs as go
RND = 3

def gen_plot(typ, traces, arts, b):
    fig = ff.create_distplot(traces, arts, bin_size=b)
    layout = go.Layout(title='Unique Word Ratios by '+typ)
    fig['layout'].update(layout)
    offline.iplot(fig)
    
def unique_words_hist(artist_obj_list, all_feat_artist=True, song_or_verse='verse', b=.01):
    verse_traces = []
    song_traces = []
    art_order = []
    offline.init_notebook_mode(connected=True)
    for art in artist_obj_list:
        art_order.append(art.name)
        #by verse
        uniq_vs = []
        #by song
        uniq_ss = []
        for sng in art.songs:
            one_song_uniqs = set()
            one_song_all = []
            for seg in sng.segments:
                lab = seg.label.lower()
                if type(seg) == verse and (all_feat_artist or art.name.lower() in lab or re.match('[^a-z0-9](verse|bridge)[^a-z0-9]', lab)): 
                    #add this individual verse ratio
                    uniq_vs.append(len(seg.unique_words)/len(seg.all_words))
                    #add unique words in verses by artist
                    one_song_uniqs = one_song_uniqs|seg.unique_words
                    #add words like a per capita
                    one_song_all.extend(seg.all_words)
            if one_song_uniqs and one_song_all:
                #then add the ratio to verses by song by artist
                uniq_ss.append(len(one_song_uniqs)/len(one_song_all))
                
        verse_traces.append(uniq_vs)
        song_traces.append(uniq_ss)
    if song_or_verse.lower() == 'verse':
        gen_plot('Verse', verse_traces, art_order, b)
    elif song_or_verse.lower() == 'song':
        gen_plot('Song', song_traces, art_order, b)
    else:
        gen_plot('Verse', verse_traces, art_order, b)
        gen_plot('Song', song_traces, art_order, b)

#my favorite funciton of all time tbh
def unique_verses_bar(artist_obj_list, all_feat_artist=True, verse_count = 10):
    #go through all artists, make a trace, plot them all
    #also works for ind artist
    traces = []
    offline.init_notebook_mode(connected=True)
    for art in artist_obj_list:
        all_verses = []
        for v in art.verses:
            lab = v.label.lower()
            if all_feat_artist or art.name.lower() in lab or re.match('[^a-z0-9](verse|bridge)[^a-z0-9]', lab):
                all_verses.append((len(v.unique_words)/len(v.all_words), v.content, len(v.all_words)))
                
        all_verses = sorted(all_verses, reverse=True)[:verse_count]
        ys = []
        xs = []
        content = []
        for dex, a_v in enumerate(sorted(all_verses)):
            con = re.sub('\n+', '<br>',a_v[1]).rstrip('<br>')
            xs.append(a_v[2])
            content.append(con+'<br>('+str(round(a_v[0], RND))+')')
                
        trace = go.Bar(x=xs,
                orientation = 'h',
                text=content,
                #doesn't do anything right now
                textposition='bottom',
                width=.9,
                hoverinfo='text',
                name=art.name)
        traces.append(trace)
        #on to next artist if there is one
    
    layout = go.Layout(title='Top Unique Verses',
                       barmode='stack',
                       hovermode='closest',
                       #want solution to text alignment left
                       #https://stackoverflow.com/questions/50003531/r-plotly-hover-label-text-alignment
                    xaxis=dict(title='Words in Verse',
                                autorange=True,
                                zeroline=False,
                                showline=False),
                    yaxis=dict(title='(Unique/All) Words per Verse',
                                autorange=True,
                                zeroline=False,
                                showline=False,
                                showticklabels=False))
    fig = go.Figure(data=traces, layout=layout)
    offline.iplot({'data': traces, 'layout': layout})