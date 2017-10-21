from bokeh.client import push_session
from bokeh.embed import server_session
from bokeh.plotting import figure, curdoc

plot = figure()
plot.circle([1,2], [3,4])

session = push_session(curdoc())
script = server_session(plot, session_id=session.id)