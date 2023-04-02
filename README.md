# How to Use NVB

To use NVB, first run `mlp.py` and see how it works.

# What is NVB

NNVisBuilder is a programming toolkit designed to enable users to easily and quickly build interactive visual analytic interfaces for various neural networks. While we provide some interface templates, they are not a core part of NNVisBuilder. NNVisBuilder is a visualization system that helps users build their own interfaces.

# How to Code with NVB to Build Your Own Interface

NVB is like a visual analytics framework, but its visualization is based on views. To add a view to the interface, simply create an object for that type of view. For example:

`view = ScatterPlot(data, [100, 100], [200, 200])`

Generally, views need to be bound to data, which specifies how elements are displayed within the view. For instance, a scatter plot consists of a collection of points, and its first parameter specifies the positions of those points. In addition to positions, the ScatterPlot can also specify colors, sizes, etc., all of which can be defined through data.

Furthermore, users can specify additional view information such as position and size. For example, the above statement specifies a position of `[100, 100]` and a size of `[200, 200]`.

The binding between views and data in NVB is dynamic. As data changes, views change as well, providing the foundation for NVB's interactive functionality.

If you want to implement some interactive functionality in NVB, you don't need to write complex code to modify the interface. Simply modify the data, and the associated views will update accordingly.

NVB's views require data to be wrapped in a Data class to achieve dynamic binding. For instance, if `a` is a numpy array representing all the points' positions, wrap it using:

`data = Data(a)`

and then pass it to the view. Not all views require wrapped data, and users may choose not to wrap data if they don't need dynamic relationships.

Defining interactive methods is similar to JavaScript:

`view.onclick(f)`

Here, `f` is the event handler function, and the function's parameter depends on the specific view. Some generalities exist to help users remember, while some flexibility exists to facilitate specialized design.

Therefore, data, views, and interactions are the three basic modules of NVB. To use NVB, users need to prepare data, define views, and specify interactions.

NVB has some specific designs for these three modules:

1. Data:
2. Views:
3. Interactions:

As a toolkit specialized for neural networks, NNVisBuilder is designed to:

1. Abstract the interface representation model, which summarizes the data processing and interaction processes of the interface as a flow chart
2. Encapsulate the process of obtaining commonly used data for neural network visualization, such as network activation, gradients, and connections

Further explanations, detailed instructions, user manuals, and API documents will be provided in the future.





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



