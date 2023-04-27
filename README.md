# How to Use NVB

To use NVB, first run `mlp.py` and see how it works. If you run `cnn.py`, the relevant dataset will be automatically downloaded first. If you run `lstmvis.py`, you need to manually download eng-fra.txt from the data folder at https://pan.baidu.com/s/1O8_qOEgoXKgUK0CyxIc3-g?pwd=ws8s and place it in the data folder, and download encoder.pth and decoder.pth from the model folder and place them in the model folder.

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

## Interaction

Defining interactive methods is similar to JavaScript:

`view.onclick(f)`

The f here is the event handler function of the following form:

```def f(value):
   data.update(value)
```
What `f`'s argument takes depends on the specific view. There will be some commonality for ease of use and some flexibility for specialized designs.

Specifically, `f` allows for different numbers of arguments to be passed. For example, in a HeatMap, if the Selector is set to select one or more rows (i.e., selecting on the first dimension of the tensor), then value will be the row number or a list of row numbers. If the Selector is set to select specific points (such as the point at the first row and second column <1,2>) or a list of points, then the definition of f is a function that accepts two arguments, and these two arguments will represent the x and y coordinates of the selected point. Sometimes, for the same Selector, `f` can also be defined to accept different numbers of arguments, depending on the specific view. These details will be reflected in the user manual later.

In `f`, data or some transformations can be modified. If the types of value and data are the same (the tensor order is the same), calling update will directly replace the value with the corresponding value in value. Otherwise, if data is a vector and value is a scalar, if value is in data, it will be removed, otherwise it will be added. This is a convenience we provide based on practice.

Views can define a Highlighter to specify how to respond to selected information. For example, for a scatter plot, it can be specified to enlarge the selected point or modify the color of the point. NVB includes the selected information in the Highlighter of the view, so if two views are bound to the same Highlighter, their selections will be passed on.

NVB defines default event handling functions for views. This function will use the value passed to f to modify the selection information of the view's Highlighter. At the same time, NVB allows mapping functions to be added for selected information. When the selected information changes, all corresponding mapping functions will be called automatically. For example, the following code:
```
def f(value):
    highlighter = view.highlighter
    highlighter.update(value)
    g(highlighter.value)
view.on_click(f)
```
And the code:
```
view.highlighter.add_mapping(g)
```
have the same effect.

## Structure

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
   - NVB also provides some widgets to help users build control panels, which are generally similar to views, but do not require binding data.
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

# Some additional explanations:

1. Composite view: By overlapping some existing views, part of a composite view can be generated.
2. Multiple models: If data from multiple models is needed, simply create multiple builders. Finally, calling the run method of one of the builders can generate the interface.
3. Other transformations: Other transformations like TSNE can also be added to the relationship tree (participating in dynamic response after modifying the data). by using `data.apply_transform(OtherTransform(tsne))`. If the TSNE transformation does not need to record relationships, it can be used directly with `tsne(data)`.

Further explanations, detailed instructions, user manuals, and API documents will be provided in the future.

\
\
\
\
\
\
The Chinese below corresponds to the English above
以上英文都是从中文翻译过去的
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

## Interaction

定义交互的方法就像js一样，

`view.onclick(f)`

这里的`f`是类似以下形式的事件处理函数：

```
def f(value):
   data.update(value)
```

`f`的参数传入的什么取决于具体的视图。会有一些共性，方便用户记住，也会有一些灵活性，方便特化设计。

具体而言，`f`允许传入不同数量的参数。例如，在HeatMap中，如果指定Selector为选中一（多）行（也就是在张量的第一维度上选择），那么value会是行数或者行数的列表。如果Selector指定为选择特定的点（例如第一行第二列<1,2>）或点的列表，那么定义f是接受两个参数的函数，这两个参数会分别表示选中点的x和y坐标。 有时候，对于同一种Selector，也可以定义接受不同数量参数的`f`，这取决于具体的视图，后续这些细节会在用户手册中体现。

在f中可以对数据或某些变换进行修改。如果value和data的类型相同（张量阶数相同），调用update会直接将值替换为value对应值。否则，如果data是向量，value是标量，那么如果value在data中，就会被删除，反之会被加入。这是我们根据实践提供的一个方便。

视图可以定义Highlighter来指定其如何对选中信息进行响应。例如，对于散点图，可以指定放大选中点，或修改点的颜色。NVB将选中信息包含在视图的Highlighter中，这样如果两个视图绑定同一个Highlighter，那么他们的选中会传递。

NVB为视图定义了默认的事件处理函数，这个函数会使用上面传给f的value修改视图的Highlighter的选中信息。同时，NVB允许为选中信息添加映射函数，当选中信息发生变化时，对应的所有映射函数会自动被调用。例如下面的代码：
```angular2html
def f(value):
    highlighter = view.highlighter
    highlighter.update(value)
    g(highlighter.value)
view.on_click(f)
```

和代码
```angular2html
   view.highlighter.add_mapping(g)
```
效果是相同的。

## Structure
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
   - NVB同样提供一些小控件帮助用户构建控制面板，这些小控件的使用总体上和视图相似，但是不需要绑定数据。
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

# 一些补充说明
1. 复合视图：通过重叠一些已有视图，可以产生一部分复合型视图。
2. 多模型：如果需要获取多个模型的数据，那么只需要创建多个Builder即可。最后调用其中一个Builder的run就可以生成界面。
3. 其他变换：像TSNE这样的变换也可以添加到关系树（它会参与修改数据后发生的动态响应）中，使用data.apply_transform(OtherTransform(tsne)即可。如果tsne变换不需要记录关系，直接使用tsne(data)即可。

具体的介绍和详细说明和用户手册和api文档将在后续慢慢补充。。。
