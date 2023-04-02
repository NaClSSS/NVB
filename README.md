# How to Use NVB
To use NVB, first try running `mlp.py` to see how it works.

# What is NVB
NNVisBuilder is a programming toolkit.
Our design goal is to enable users to easily and quickly build interactive visual analytic interfaces for various neural networks.

We will provide some templates for of interfaces, but this is not part of the core of NNVisBuilder. NNVisBuilder is like a visualization system that helps you build interfaces. You can design your own interfaces.

# How to code with NVB to build your own interface
NVB就像可视分析框架，但是它的可视化是以视图为基本单位。你想要往界面上添加什么视图，就创建一个那种视图的对象就好。
例如：

`view = ScatterPlot(data, [100, 100], [200, 200])`

一般视图上都是需要绑定数据的。这些数据指定了视图里的元素如何绘制。例如，散点图里包含了一堆点，它的第一个参数就是指定这些点的位置的。
除了指定点的位置，ScatterPlot在创建时还可以指定点的颜色，大小，等等。这些都是可以通过数据指定的。

除此之外，还可以指定一些视图的信息，例如位置，大小等等。就像上面那句就指定了位置在[100, 100], 大小为[200, 200]。

NVB的视图和数据的绑定是动态的。当数据在后续被修改时，视图也会发生变化。这为NVB的交互功能提供了基础。

在NVB中，如果你想实现一些交互功能，你不需要去编写复杂的修改界面的代码，而只需要去修改数据就好，这样它关联的视图就会变化。

NVB的视图上使用的数据需要用一个Data类进行包装，才能实现动态绑定。例如a是一个表示所有点位置的numpy数组，那么使用

`data = Data(a)`

将它包装，然后传给视图就可以了。当然，不是所有视图使用的数据都需要包装，如果你不需要这种动态关系，你可以不包装。

定义交互的方法就像js一样，

`view.onclick(f)`

这里f就是事件处理函数，f的参数传入的什么取决于具体的视图。会有一些共性，方便用户记住，也会有一些灵活性，方便特化设计。

所以数据、视图、交互三个模块就是NVB的基础结构。如果你要使用NVB，你的编码方式就是准备好数据，然后定义视图，然后定义交互。

NVB在三个模块上分别有一些设计：
1. 数据：
2. 视图：
3. 交互：

NVB作为专门为神经网络设计的工具包，这个专门体现在：
1. 我们抽象出了一个表示界面的模型，这个模型将界面上的数据处理和交互过程总结为一个流程图
2. 我们为神经网络可视化时常用的数据封装了获取过程，例如网络激活，梯度，连接等

具体的介绍和详细说明和用户手册和api文档将在后续慢慢补充。。。



