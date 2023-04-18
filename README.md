# Some model and data here
https://pan.baidu.com/s/1O8_qOEgoXKgUK0CyxIc3-g?pwd=ws8s 

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

NVB has some designs in three modules, and these designs based on our data abstraction are our main contributions, or the main differences that make NVB different from other visualization frameworks (in building neural network visual analysis interfaces)：

1. Data:
   - NVB encapsulates the common process of data acquisition and abstracts the data as data classes. The binding relationship between data and views can be achieved based on these data classes.
   - NVB provides common transformations on data. The transformations using NVB will automatically record the transformation relationship (forming a transformation relationship graph), and other data will also change accordingly when some data change.
   - Dynamic binding and transformation relationship graph provide a foundation for users to interact at a higher level.
2. Views:
   - Users can specify different attributes of the views when defining them, including some common attributes such as view position and size, and some specific attributes of the views, such as the position and color of each point in a scatter plot.
   - The specific attributes of the views can be specified as an NVB data, which can achieve dynamic binding. If dynamic binding is not needed, the value of the attribute can be directly specified, and there is no need to wrap the value as an NVB data.
   - Users only need to specify the attributes of the views, and the system will automatically generate the visualization. Users do not need to care about the visualization aspect or write visualization code.
   - If users need to customize the view, they can define their own view based on NVB specifications (currently referring to existing view classes), and then use it like using an existing view.
3. Interaction:
   - Based on dynamic binding, users can achieve all types of interaction by modifying the data, transformations or selection information corresponding to other views in the event handling of the interaction. This is **the most fundamental difference in using NVB for coding**, based on our data abstraction.
   - Selection information is another factor that affects the display result of the views, usually represented as a selected subset of a certain dimension of the data. For example, a heatmap corresponds to a two-dimensional tensor data, and one row (multiple rows) or one column (multiple columns) can be selected.
   - Selection information may undergo some transformations when it affects the data or selection information of other views. NVB provides templates for common transformations to further facilitate user coding.
   - NVB defines different selectors for different selection methods, and each type of view has multiple preset selectors, and users can also customize selectors.
   - NVB abstracts the response of highlighted information in the view as Highlighter, and each type of view has multiple preset highlighters, and users can also customize highlighters.
   - NVB provides Multi-Selector and Multi-Highlighter, which allow users to obtain more selection methods and interaction response modes through combination.
   - The specific description of Selector, Highlighter, Multi-Selector, and Multi-Highlighter is to be supplemented.

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

NVB在三个模块上分别有一些设计，这些基于我们的数据抽象的设计是我们的主要贡献，或者说是使得NVB区别于其他可视化框架（在构建神经网络可视分析界面上）的主要不同之处：

1. 数据：
   - NVB封装了常见的数据的获取过程，同时将数据抽象为数据类，基于数据类可以实现数据和视图的绑定关系。
   - NVB提供了数据上的常见变换，使用NVB的变换会自动记录变换关系（形成变换关系图），在某些数据改变时其他数据也会相应改变。
   - 动态绑定和变换关系图为用户在高层编码交互提供了基础。
2. 视图：
   - 用户在定义视图时可以指定视图的不同属性，包含一些通用属性例如视图位置，大小等；也包含一些视图的特有属性，例如对于散点图，可以指定每个点的位置，颜色等。
   - 视图的特有属性可以指定为一个NVB数据，这样可以实现动态绑定；如果不需要动态绑定关系，也可以直接指定属性的值，不需要将值包装为NVB数据。
   - 用户只需要指定视图的属性，系统会自动生成可视化，用户无需关心可视化方面的内容，无需编写可视化的代码。
   - 如果用户需要自定义视图，可以基于NVB的规范（暂时参照已有视图类获取）来定义自己的视图，然后像使用原有视图一样使用它。
3. 交互：
   - 基于动态绑定，用户可以通过在交互处理事件中修改其他视图对应的数据、变换或选中信息来实现所有的交互方式。这是基于我们的数据抽象得出的**使用NVB编码时最核心的不同**。
   - 选中信息是影响视图显示结果的另一个因素，通常表示为数据的某个维度的选中子集。例如一个热力图对应二维张量数据，可以选中其中的一行（多行）或一列（多列）。
   - 选中信息在影响其他视图的数据或者选中信息时，可能经过一些转换。NVB会为常见的转换提供模板，进一步方便用户编码。
   - NVB为不同的选中方式定义了不同的Selector，每种视图具有多种预设的Selector，用户也可以自定义Selector
   - NVB将视图中对高亮信息的响应抽象为Highlighter，每种视图具有多种预设的Highlighter，用户也可以自定义Highlighter
   - NVB提供了Multi-Selector, Multi-Highlighter让用户能通过组合得到更多的选中方式和交互响应模式。
   - Selector，Highlighter和Multi-Selector，Multi-Highlighter的具体描述待补充。

NVB作为专门为神经网络设计的工具包，这个专门体现在：
1. 我们抽象出了一个表示界面的模型，这个模型将界面上的数据处理和交互过程总结为一个流程图
2. 我们为神经网络可视化时常用的数据封装了获取过程，例如网络激活，梯度，连接等

具体的介绍和详细说明和用户手册和api文档将在后续慢慢补充。。。

