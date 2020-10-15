from vtk import *
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
import wx
from random import*


class Rectangulo:
    def __init__(self, x, y, z, a, b, c):
        self.x = x
        self.y = y
        self.z = z
        self.w = a
        self.h = b
        self.p = c

    def contains(self, point):
        return (point.x <= self.x+self.w and point.x >= self.x-self.w and self.y+self.h >= point.y and point.y >= self.y-self.h and self.z+self.p >= point.z and point.z >= self.z-self.p)


    def intersect(self, range): # range es otro cubo
        return (range.x + range.w > self.x - self.w or range.x - range.w < self.x + self.w or range.y + range.h > self.y - self.h or range.y - range.h < self.y + self.h or range.z + range.p > self.z - self.p or range.z - range.p < self.z + self.p)





class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Octree:
    def __init__(self, cub, tam, color, color_punto):
        self.cubo = cub
        self.capacidadMaxima = tam
        self.points = []
        self.divided = False
        self.hijos = []
        self.color = color
        self.color_punto = color_punto

    def insert(self, point, puntosG, estado, colores):
        """
        puntosG almacenará todos los nuevos puntosG creados, para ser dibujados
        El retorno de esta funcion se divide en 2 partes, primero si es posible agregar un valor considerando los
        paramtros, el segundo es, el color del punto
        """
        if not self.cubo.contains(point):
            return

        if len(self.points) < self.capacidadMaxima:
            self.points.append(point)
            estado[0] = True
            colores.append(self.color_punto)
            return
        else:
            if not self.divided:
                self.subdivide(puntosG)

        self.hijos[0].insert(point, puntosG, estado, colores)
        self.hijos[1].insert(point, puntosG, estado, colores)
        self.hijos[2].insert(point, puntosG, estado, colores)
        self.hijos[3].insert(point, puntosG, estado, colores)
        self.hijos[4].insert(point, puntosG, estado, colores)
        self.hijos[5].insert(point, puntosG, estado, colores)
        self.hijos[6].insert(point, puntosG, estado, colores)
        self.hijos[7].insert(point, puntosG, estado, colores)


    def subdivide(self, puntosG):
        # puntosG almacenará todos los nuevos puntosG creados, para ser dibujados en el vtk
        x = self.cubo.x
        y = self.cubo.y
        z = self.cubo.z
        w = self.cubo.w / 2
        h = self.cubo.h / 2
        p = self.cubo.p / 2

        neup = Rectangulo(x + w, y + h, z + p, w, h, p)
        noup = Rectangulo(x - w, y + h, z + p, w, h, p)
        seup = Rectangulo(x + w, y + h, z - p, w, h, p)
        soup = Rectangulo(x - w, y + h, z - p, w, h, p)

        nedown = Rectangulo(x + w, y - h, z + p, w, h, p)
        nodown = Rectangulo(x - w, y - h, z + p, w, h, p)
        sedown = Rectangulo(x + w, y - h, z - p, w, h, p)
        sodown = Rectangulo(x - w, y - h, z - p, w, h, p)

        self.hijos.append(Octree(neup, self.capacidadMaxima, self.color.next_color(), self.color_punto.next_color_punto()))
        self.hijos.append(Octree(nedown, self.capacidadMaxima, self.hijos[0].color.next_color(), self.hijos[0].color_punto.next_color_punto()))
        self.hijos.append(Octree(noup, self.capacidadMaxima, self.hijos[1].color.next_color(), self.hijos[1].color_punto.next_color_punto()))
        self.hijos.append(Octree(nodown, self.capacidadMaxima, self.hijos[2].color.next_color(), self.hijos[2].color_punto.next_color_punto()))
        self.hijos.append(Octree(seup, self.capacidadMaxima, self.hijos[3].color.next_color(), self.hijos[3].color_punto.next_color_punto()))
        self.hijos.append(Octree(sedown, self.capacidadMaxima, self.hijos[4].color.next_color(), self.hijos[4].color_punto.next_color_punto()))
        self.hijos.append(Octree(soup, self.capacidadMaxima, self.hijos[5].color.next_color(), self.hijos[5].color_punto.next_color_punto()))
        self.hijos.append(Octree(sodown, self.capacidadMaxima, self.hijos[6].color.next_color(), self.hijos[6].color_punto.next_color_punto()))

        puntosG.append(Octree(neup, self.capacidadMaxima, self.color.next_color(), self.color_punto.next_color_punto()))
        puntosG.append(Octree(nedown, self.capacidadMaxima, self.hijos[0].color.next_color(), self.hijos[0].color_punto.next_color_punto()))
        puntosG.append(Octree(noup, self.capacidadMaxima, self.hijos[1].color.next_color(),self.hijos[1].color_punto.next_color_punto()))
        puntosG.append(Octree(nodown, self.capacidadMaxima, self.hijos[2].color.next_color(),self.hijos[2].color_punto.next_color_punto()))
        puntosG.append(Octree(seup, self.capacidadMaxima, self.hijos[3].color.next_color(),self.hijos[3].color_punto.next_color_punto()))
        puntosG.append(Octree(sedown, self.capacidadMaxima, self.hijos[4].color.next_color(),self.hijos[4].color_punto.next_color_punto()))
        puntosG.append(Octree(soup, self.capacidadMaxima, self.hijos[5].color.next_color(),self.hijos[5].color_punto.next_color_punto()))
        puntosG.append(Octree(sodown, self.capacidadMaxima, self.hijos[6].color.next_color(),self.hijos[6].color_punto.next_color_punto()))
        self.divided = True

    

    def query(self, cub, found):

        if not self.cubo.intersect(cub):
            return

        for punt in self.points:
            if cub.contains(punt):
                found.append(punt)

        if self.divided:
            self.hijos[0].query(cub, found)
            self.hijos[1].query(cub, found)
            self.hijos[2].query(cub, found)
            self.hijos[3].query(cub, found)
            self.hijos[4].query(cub, found)
            self.hijos[5].query(cub, found)
            self.hijos[6].query(cub, found)
            self.hijos[7].query(cub, found)





class AsignarColor:
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.inicial_a = d
        self.inicial_b = e
        self.inicial_c = f

    def next_color(self):
        extra = None
        if self.a - 0.02 >= 0:
            extra = AsignarColor(self.a - 0.02, self.b, self.c, self.inicial_a, self.inicial_b, self.inicial_c)
        elif self.b - 0.02 >= 0:
            extra = AsignarColor(self.a, self.b-0.02, self.c, self.inicial_a, self.inicial_b, self.inicial_c)
        else:
            if self.c - 0.02 >= 0:
                extra = AsignarColor(self.a, self.b, self.c-0.02, self.inicial_a, self.inicial_b, self.inicial_c)
            else:
                extra = AsignarColor(self.inicial_a - 0.05, self.inicial_b - 0.05, self.inicial_c - 0.05, self.inicial_a - 0.05, self.inicial_b - 0.05, self.inicial_c - 0.05)
        return extra


    def next_color_punto(self):
        extra = None
        if self.a + 0.15 < 1:
            extra = AsignarColor(self.a + 0.15, self.b, self.c, self.inicial_a, self.inicial_b, self.inicial_c)
        elif self.b + 0.15 < 1:
            extra = AsignarColor(self.a, self.b+0.15, self.c, self.inicial_a, self.inicial_b, self.inicial_c)
        else:
            if self.c + 0.15 < 1:
                extra = AsignarColor(self.a, self.b, self.c+0.15, self.inicial_a, self.inicial_b, self.inicial_c)
            else:
                extra = AsignarColor(self.inicial_a + 0.05, self.inicial_b + 0.05, self.inicial_c + 0.05, self.inicial_a + 0.05, self.inicial_b + 0.05, self.inicial_c + 0.05)
        return extra


class MostrarOctree(wx.Frame):
    def __init__(self, parent, id):

        wx.Frame.__init__(self, parent, id, 'Examen_Estructura de Datos Avanzados', size=(1024, 720))

        # Valores que seran usados para agregar y/o consultar

        self.Val_X = None
        self.Val_Y = None
        self.Val_Z = None
        self.Tamanho_Cubo = None
        # self.varbool=False
        self.actor1=None
        # .........................................................

        #Generador del menu
        menuBar = wx.MenuBar()

        menuFile = wx.Menu()
        itemAdd = menuFile.Append(-1, "&Añadir_Punto", "Agregar punto al cubo")
        itemQuery = menuFile.Append(-1, "&Consultar", "Consutar en un rango")
        itemQuit = menuFile.Append(-1, "&Quit", "Quit application")
        self.Bind(wx.EVT_MENU, self.Salir, itemQuit)

        self.Bind(wx.EVT_MENU, self.Agregar, itemAdd)
        self.Bind(wx.EVT_MENU, self.Consultar, itemQuery)
        self.Bind(wx.EVT_MENU, self.Salir, itemQuit)

        menuBar.Append(menuFile, "&Opciones")
        self.SetMenuBar(menuBar)
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(2)
        self.statusBar.SetStatusWidths([-4, -1])

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(1, 1, 1)
 
        #Creacion del octree
        # Y genereacion de puntos aleatorios en el octree
        self.arbol = Octree(Rectangulo(80, 80, 80, 80, 80, 80), 4, AsignarColor(1, 1, 1, 1, 1, 1), AsignarColor(0, 0, 0, 0, 0, 0))
        self.Create_Cubo(80, 80, 80, 80, 80, 80, 1, 1, 1,0.1)
        for i in range(0,20):
            punto_color = []
            puntosG=[]
            val=[False]
            val1=randrange(150)
            val2=randrange(150)
            val3=randrange(150)
            p=Point(val1,val2,val3)
            self.arbol.insert(p, puntosG, val, punto_color)
            for occt in puntosG:
                    self.Create_Cubo(occt.cubo.x, occt.cubo.y, occt.cubo.z, occt.cubo.w, occt.cubo.h, occt.cubo.p, occt.color.a, occt.color.b, occt.color.c,0.1)
            self.Create_Punto(float(val1), float(val2), float(val3), punto_color[0].a, punto_color[0].b, punto_color[0].c)
        # p = Point(float(self.Val_X), float(self.Val_Y), float(self.Val_Z))
        #self.rwi=wxVTKRenderWindow(self, 0)

        self.rwi = wxVTKRenderWindow(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.rwi, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        self.rwi.Enable(1)
        self.rwi.GetRenderWindow().AddRenderer(self.ren)

    def Create_Cubo(self, x1, y1, z1, x, y, z, a, b, c, d):
        # self.varbool=boolean
        cubooo = vtkCubeSource()
        cubooo.SetCenter(x1, y1, z1)
        cubooo.SetXLength(x*2)
        cubooo.SetYLength(y*2)
        cubooo.SetZLength(z*2)
        CubeMapper = vtkPolyDataMapper()
        CubeMapper.SetInputConnection(cubooo.GetOutputPort())
        CubeActor = vtkActor()

        CubeActor.GetProperty().SetColor(a, b, c)
        CubeActor.GetProperty().SetOpacity(d)
        CubeActor.SetMapper(CubeMapper)
        self.ren.AddActor(CubeActor)

        # boolean=True

        return CubeActor


    def delete_Cubo(self, actor):
        self.ren.RemoveActor(actor)


    def Create_Punto(self, a, b, c, color_1, color_2, color_3):

        source = vtk.vtkSphereSource()
        source.SetCenter(a, b, c)
        source.SetRadius(2)
        source.SetPhiResolution(10)
        source.SetThetaResolution(10)
        # mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(source.GetOutput())
        else:
            mapper.SetInputConnection(source.GetOutputPort())

        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color_1, color_2, color_3)
        actor.GetProperty().SetOpacity(0.8)
        # the render is a 3D Scene
        self.ren.AddActor(actor)

    def Agregar(self, event):
        dlg = wx.TextEntryDialog(self, 'Ingrese Posicion X', 'Posicion X')
        if dlg.ShowModal() == wx.ID_OK:
            self.Val_X = dlg.GetValue()
            dlg1 = wx.TextEntryDialog(self, 'Ingrese Posicion Y', 'Posicion Y')
            if dlg1.ShowModal() == wx.ID_OK:
                self.Val_Y = dlg1.GetValue()
                dlg2 = wx.TextEntryDialog(self, 'Ingrese Posicion Z', 'Posicion Z')
                if dlg2.ShowModal() == wx.ID_OK:
                    self.Val_Z = dlg2.GetValue()
                else:
                    return
                dlg2.Destroy()
            else:
                return
            dlg1.Destroy()
        else:
            return
        dlg.Destroy()

        p = Point(float(self.Val_X), float(self.Val_Y), float(self.Val_Z))
        puntosG = []
        val = [False]
        punto_color = []
        self.arbol.insert(p, puntosG, val, punto_color)
        if val[0]:
            if len(puntosG) != 0:
                for occt in puntosG:
                    self.Create_Cubo(occt.cubo.x, occt.cubo.y, occt.cubo.z, occt.cubo.w, occt.cubo.h, occt.cubo.p, occt.color.a, occt.color.b, occt.color.c, 0.1)
            self.Create_Punto(float(self.Val_X), float(self.Val_Y), float(self.Val_Z), punto_color[0].a, punto_color[0].b, punto_color[0].c)
            #print(str(punto_color[0].a) + " " + str(punto_color[0].b) + " " + str(punto_color[0].c))

    def Consultar(self, event):
        dlg = wx.TextEntryDialog(self, 'Posicion X del Centro del rango a consultar: ', 'Posicion X')
        if dlg.ShowModal() == wx.ID_OK:
            self.Val_X = dlg.GetValue()
            dlg1 = wx.TextEntryDialog(self, 'Posicion Y del Centro del rango a consultar:', 'Posicion Y')
            if dlg1.ShowModal() == wx.ID_OK:
                self.Val_Y = dlg1.GetValue()
                dlg2 = wx.TextEntryDialog(self, 'Posicion Z del Centro del rango a consultar:', 'Posicion Z')
                if dlg2.ShowModal() == wx.ID_OK:
                    self.Val_Z = dlg2.GetValue()
                    dlg4 = wx.TextEntryDialog(self, 'Longitud del rango a preguntar', 'Perimetro')
                    if dlg4.ShowModal() == wx.ID_OK:
                        self.Tamanho_Cubo = dlg4.GetValue()
                    else:
                        return
                else:
                    return
                dlg2.Destroy()
            else:
                return
            dlg1.Destroy()
        else:
            return
        dlg.Destroy()
        # varbool=False

        # punto_color=[]
        answer = []
        if self.actor1==None:
            self.actor1=self.Create_Cubo(float(self.Val_X), float(self.Val_Y), float(self.Val_Z), float(self.Tamanho_Cubo)/2, float(self.Tamanho_Cubo)/2, float(self.Tamanho_Cubo)/2, 0.0, 0.085, 0.532,0.5)
            newP=Rectangulo(float(self.Val_X), float(self.Val_Y), float(self.Val_Z), float(self.Tamanho_Cubo)/2, float(self.Tamanho_Cubo)/2, float(self.Tamanho_Cubo)/2)
            self.arbol.query(newP, answer)
            print(len(answer))
            for p in answer:
                print("p("+str(p.x)+" , "+ str(p.y)+" , "+str(p.z)+")")
            respuesta = "Cantidad de puntos en el rango indicado: " + str(len(answer))
            mostrar_respuesta = wx.MessageBox(respuesta, "Respuesta", wx.OK)
        else:
            self.delete_Cubo(self.actor1)
            self.actor1=None
            self.actor1=self.Create_Cubo(float(self.Val_X), float(self.Val_Y), float(self.Val_Z), float(self.Tamanho_Cubo)/2, float(self.Tamanho_Cubo)/2, float(self.Tamanho_Cubo)/2, 0.0, 0.085, 0.532,0.5)
            newP=Rectangulo(float(self.Val_X), float(self.Val_Y), float(self.Val_Z), float(self.Tamanho_Cubo)/2, float(self.Tamanho_Cubo)/2, float(self.Tamanho_Cubo)/2)
            self.arbol.query(newP, answer)
            print(len(answer))
            for p in answer:
                print("p("+str(p.x)+" , "+ str(p.y)+" , "+str(p.z)+")")
            respuesta = "Cantidad de puntos en el rango indicado: " + str(len(answer))
            mostrar_respuesta = wx.MessageBox(respuesta, "Respuesta", wx.OK)
        
            




    def Salir(self, event):
        self.Close()


# start the wx loop
app = wx.App()
frame = MostrarOctree(None, -1)
frame.Show()
app.MainLoop()
