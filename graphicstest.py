import pyglet
window = pyglet.window.Window()
label = pyglet.text.Label('Aloha Wrld',
                          font_name='Calibri',
                          font_size=32,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
@window.event
def on_draw():
    window.clear()
    label.draw()
    pyglet.graphics.draw(2, pyglet.gl.GL_POINTS,
                         ('v2i', (10, 15, 30, 35))
                         )
pyglet.app.run()