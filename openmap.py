#key: AIzaSyAGpAezj2glYNnuog_TtqeznMRxEFijB7c

WIDTH = 1000
HEIGHT = 800

LATITUDE  =  32.8288
LONGITUDE = -83.6496
ZOOM = 15
MAPTYPE = 'roadmap'

class UI(Tk):

    def __init__(window):

        Tk.__init__(window)

        window.geometry('%dx%d+500+500' % (WIDTH,HEIGHT))
        window.title('GooMPy')

        window.canvas = Canvas(window, width=WIDTH, height=HEIGHT)

        window.canvas.pack()

        window.bind("<Key>", window.check_quit)
        window.bind('<B1-Motion>', window.drag)
        window.bind('<Button-1>', window.click)

        window.label = Label(window.canvas)

        window.radiogroup = Frame(window.canvas)
        window.radiovar = IntVar()
        window.maptypes = ['roadmap', 'terrain', 'satellite', 'hybrid']
        window.add_radio_button('Road Map',  0)
        window.add_radio_button('Terrain',   1)
        window.add_radio_button('Satellite', 2)
        window.add_radio_button('Hybrid',    3)

        window.zoom_in_button  = window.add_zoom_button('+', +1)
        window.zoom_out_button = window.add_zoom_button('-', -1)

        window.zoomlevel = ZOOM

        maptype_index = 0
        window.radiovar.set(maptype_index)

        window.goompy = GooMPy(WIDTH, HEIGHT, LATITUDE, LONGITUDE, ZOOM, MAPTYPE)

        window.restart()

    def add_zoom_button(window, text, sign):

        button = Button(window.canvas, text=text, width=1, command=lambda:window.zoom(sign))
        return button

    def reload(window):

        window.coords = None
        window.redraw()

        window['cursor']  = ''


    def restart(window):

        # A little trick to get a watch cursor along with loading
        window['cursor']  = 'watch'
        window.after(1, window.reload)

    def add_radio_button(window, text, index):

        maptype = window.maptypes[index]
        Radiobutton(window.radiogroup, text=maptype, variable=window.radiovar, value=index, 
                command=lambda:window.usemap(maptype)).grid(row=0, column=index)

    def click(window, event):

        window.coords = event.x, event.y

    def drag(window, event):

        window.goompy.move(window.coords[0]-event.x, window.coords[1]-event.y)
        window.image = window.goompy.getImage()
        window.redraw()
        window.coords = event.x, event.y

    def redraw(window):

        window.image = window.goompy.getImage()
        window.image_tk = ImageTk.PhotoImage(window.image)
        window.label['image'] = window.image_tk

        window.label.place(x=0, y=0, width=WIDTH, height=HEIGHT) 

        window.radiogroup.place(x=0,y=0)

        x = int(window.canvas['width']) - 50
        y = int(window.canvas['height']) - 80

        window.zoom_in_button.place(x= x, y=y)
        window.zoom_out_button.place(x= x, y=y+30)

    def usemap(window, maptype):

        window.goompy.useMaptype(maptype)
        window.restart()

    def zoom(window, sign):

        newlevel = window.zoomlevel + sign
        if newlevel > 0 and newlevel < 22:
            window.zoomlevel = newlevel
            window.goompy.useZoom(newlevel)
            window.restart()

    def check_quit(window, event):

        if ord(event.char) == 27: # ESC
            exit(0)

UI().mainloop()