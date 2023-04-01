import torch
import d3backend
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import matplotlib.pyplot as plt
# from torch.utils.tensorboard import SummaryWriter
# import tensorflow as tf
# import tensorboard as tb
# tf.io.gfile = tb.compat.tensorflow_stub.io.gfile

# ------------------------------------
IS_PERSPECTIVE = True  # 透视投影
VIEW = np.array([-1000, 1000, -1000, 1000, 200.0, 400.0])  # 视景体的left/right/bottom/top/near/far六个面
SCALE_K = np.array([1.0, 1.0, 1.0])  # 模型缩放比例
EYE = np.array([0.0, 0.0, 300.0])  # 眼睛的位置（默认z轴的正方向）
LOOK_AT = np.array([0.0, 0.0, 0.0])  # 瞄准方向的参考点（默认在坐标原点）
EYE_UP = np.array([0.0, 1.0, 0.0])  # 定义对观察者而言的上方（默认y轴的正方向）
WIN_W, WIN_H = 640, 480  # 保存窗口宽度和高度的变量
LEFT_IS_DOWNED = False  # 鼠标左键被按下
MOUSE_X, MOUSE_Y = 0, 0  # 考察鼠标位移量时保存的起始位置


def getposture():
    global EYE, LOOK_AT

    dist = np.sqrt(np.power((EYE - LOOK_AT), 2).sum())
    if dist > 0:
        phi = np.arcsin((EYE[1] - LOOK_AT[1]) / dist)
        theta = np.arcsin((EYE[0] - LOOK_AT[0]) / (dist * np.cos(phi)))
    else:
        phi = 0.0
        theta = 0.0

    return dist, phi, theta


DIST, PHI, THETA = getposture()  # 眼睛与观察目标之间的距离、仰角、方位角


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)  # 设置画布背景色。注意：这里必须是4个参数
    glEnable(GL_DEPTH_TEST)  # 开启深度测试，实现遮挡关系
    glDepthFunc(GL_LEQUAL)  # 设置深度测试函数（GL_LEQUAL只是选项之一）


def reshape(width, height):
    global WIN_W, WIN_H

    WIN_W, WIN_H = width, height
    glutPostRedisplay()


def mouseclick(button, state, x, y):
    global SCALE_K
    global LEFT_IS_DOWNED
    global MOUSE_X, MOUSE_Y

    MOUSE_X, MOUSE_Y = x, y
    if button == GLUT_LEFT_BUTTON:
        LEFT_IS_DOWNED = state == GLUT_DOWN
    elif button == 3:
        SCALE_K *= 1.05
        glutPostRedisplay()
    elif button == 4:
        SCALE_K *= 0.95
        glutPostRedisplay()


def mousemotion(x, y):
    global LEFT_IS_DOWNED
    global EYE, EYE_UP
    global MOUSE_X, MOUSE_Y
    global DIST, PHI, THETA
    global WIN_W, WIN_H

    if LEFT_IS_DOWNED:
        dx = MOUSE_X - x
        dy = y - MOUSE_Y
        MOUSE_X, MOUSE_Y = x, y

        PHI += 2 * np.pi * dy / WIN_H
        PHI %= 2 * np.pi
        THETA += 2 * np.pi * dx / WIN_W
        THETA %= 2 * np.pi
        r = DIST * np.cos(PHI)

        EYE[1] = DIST * np.sin(PHI)
        EYE[0] = r * np.sin(THETA)
        EYE[2] = r * np.cos(THETA)

        if 0.5 * np.pi < PHI < 1.5 * np.pi:
            EYE_UP[1] = -1.0
        else:
            EYE_UP[1] = 1.0

        glutPostRedisplay()


def keydown(key, x, y):
    global DIST, PHI, THETA
    global EYE, LOOK_AT, EYE_UP
    global IS_PERSPECTIVE, VIEW

    if key in [b'x', b'X', b'y', b'Y', b'z', b'Z']:
        if key == b'x':  # 瞄准参考点 x 减小
            LOOK_AT[0] -= 0.01
        elif key == b'X':  # 瞄准参考 x 增大
            LOOK_AT[0] += 0.01
        elif key == b'y':  # 瞄准参考点 y 减小
            LOOK_AT[1] -= 0.01
        elif key == b'Y':  # 瞄准参考点 y 增大
            LOOK_AT[1] += 0.01
        elif key == b'z':  # 瞄准参考点 z 减小
            LOOK_AT[2] -= 0.01
        elif key == b'Z':  # 瞄准参考点 z 增大
            LOOK_AT[2] += 0.01

        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\r':  # 回车键，视点前进
        EYE = LOOK_AT + (EYE - LOOK_AT) * 0.9
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\x08':  # 退格键，视点后退
        EYE = LOOK_AT + (EYE - LOOK_AT) * 1.1
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b' ':  # 空格键，切换投影模式
        IS_PERSPECTIVE = not IS_PERSPECTIVE
        glutPostRedisplay()
# ----------------------------------------


# ----self definition & combination
# ----set multiple defaults
class View:
    def __init__(self, positions=[], elements=[], sizes=[]):
        self.positions = positions
        self.elements = elements
        self.sizes = sizes

    def add(self, position, element, size):
        self.positions.append(position)
        self.elements.append(element)
        self.sizes.append(size)

    def draw(self):
        for i in range(len(self.positions)):
            self.elements[i].draw(self.positions[i])


class Point(View):
    def __init__(self, color):
        self.color = color

    def draw(self, position):
        glColor4f(*self.color)

        glVertex3f(*position, 0)


class Layout(View):
    def __init__(self, data, transform, labels, p_elements):
        """
        :param data:
        :param transform: can be str or a function which implement dimension reduction on data
        :param labels:
        :param elements: can be str or a list of Element derived from class View
        """
        positions = None
        elements = None
        if type(transform) == str:
            if transform == 'TSNE':
                positions = TSNE(n_components=2).fit_transform(data)
            elif transform == 'PCA':
                positions = PCA(n_components=2).fit_transform(data)
        elif callable(transform):
            positions = transform(data)
        if type(p_elements) == str:
            if p_elements == 'point':
                colors = plt.cm.Spectral(np.array(labels))
                elements = [Point(color) for color in colors]
        elif type(p_elements) == list:
            elements = p_elements
        print(len(positions), len(elements))
        super().__init__(positions, elements)
    def draw(self, position):
        glBegin(GL_LINE_LOOP)
        glColor4f(1.0, 0.0, 0.0, 1.0)
        position = [-1000, -1000]
        glVertex3f(position[0], position[1], 0)
        glVertex3f(position[0]+2000, position[1], 0)
        glVertex3f(position[0]+2000, position[1]+2000, 0)
        glVertex3f(position[0], position[1]+2000, 0)
        glEnd()
        glClear(GL_COLOR_BUFFER_BIT)
        glPointSize(4.0)
        glBegin(GL_POINTS)
        glColor4f(0.0, 1.0, 0.0, 1.0)
        # for i in range(len(self.positions)):
        for i in range(24):
            self.elements[i].draw(self.positions[i])
        glEnd()


class NNVis:
    def __init__(self, model, input, labels=None, inputP=None):
        self.model = model
        self.name2module = dict(model.named_modules())
        self.input = input
        self.labels = labels
        # self.grads = {}
        self.hooks = []
        self.embs = {}
        self.views = []

    def add_embedding(self, name):
        self.embs[name] = torch.Tensor([])
        def get_hook(name):
            def hook(model, input, output):
                self.embs[name] = torch.cat((self.embs[name], output.detach().cpu()), 0)
            return hook
        self.hooks.append(self.name2module[name].register_forward_hook(get_hook(name)))

    # def add_grad(self, model_layer, id, global_step):
    #     self.grads[id] = model_layer

    def add_layout(self, name, layout, position):
        self.views.append([name, layout, position])

    def run(self):
        batch_size = 16
        i = 0
        t = 256
        with torch.no_grad():
            while batch_size * (i + 1) <= t:
                print('---------- %d / %d' % (batch_size * i, t))
                a = self.input[batch_size * i:batch_size * (i + 1)]
                self.model(a.cuda())
                i += 1
            print('---------- %d / %d' % (t, t))
        torch.cuda.empty_cache()
        for hook in self.hooks:
            hook.remove()
        root = View()
        for view in self.views:
            layout = Layout(self.embs[view[0]], view[1], self.labels, 'point')
            root.add(view[2], layout, [200, 200])
        # data = [embs]
        # if self.labels is not None:
        #     data.append(self.labels.cpu().tolist())
        # else:
        #     data.append([0 for i in range(self.input.size()[0])])
        glutInit()
        displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
        glutInitDisplayMode(displayMode)

        glutInitWindowSize(WIN_W, WIN_H)
        glutInitWindowPosition(300, 200)
        glutCreateWindow('Quidam Of OpenGL')

        def draw():
            global IS_PERSPECTIVE, VIEW
            global EYE, LOOK_AT, EYE_UP
            global SCALE_K
            global WIN_W, WIN_H
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            if WIN_W > WIN_H:
                if IS_PERSPECTIVE:
                    glFrustum(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
                else:
                    glOrtho(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
            else:
                if IS_PERSPECTIVE:
                    glFrustum(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])
                else:
                    glOrtho(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glScale(SCALE_K[0], SCALE_K[1], SCALE_K[2])
            gluLookAt(
                EYE[0], EYE[1], EYE[2],
                LOOK_AT[0], LOOK_AT[1], LOOK_AT[2],
                EYE_UP[0], EYE_UP[1], EYE_UP[2]
            )
            glViewport(0, 0, WIN_W, WIN_H)
            root.draw()
            glutSwapBuffers()

        init()
        glutDisplayFunc(draw)
        # glutReshapeFunc(reshape)
        # glutMouseFunc(mouseclick)
        # glutMotionFunc(mousemotion)
        # glutKeyboardFunc(keydown)

        glutMainLoop()

        # d3backend.load_data(data, embs_p, self.input.cpu(), self.inputP)
        # d3backend.launch()
