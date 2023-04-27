from NNVisBuilder.Views import View
from backend import Container
from NNVisBuilder.GlobalVariables import *
import json
import re


def is_decimal(s):
    return bool(re.match(r'^-?\d+\.\d+$', s))


class Widget:
    idx = 0
    def __init__(self, position, size=(30, 30)):
        # **info param can be used.
        self.position = position
        self.size = size
        self.idx = Widget.idx
        Widget.idx += 1
        self.click_ = None
        Container.handler['c%d' % self.idx] = self.click
        View.widgets.append(self)

    def core(self):
        View.f.write(f"""
const w{self.idx} = d2.append('div').classed('div4', true).style('position', 'absolute');
w{self.idx}.style('width', '{self.size[0]}px')
    .style('height', '{self.size[1]}px')
    .style('left', '{self.position[0]}px')
    .style('top', '{self.position[1]}px');
        """)

    def onclick(self, f):
        self.click_ = f

    def click(self, request_args):
        value = request_args.get('value')
        View.update_list.clear()
        self.click_(value)
        return json.dumps(View.update_list)


class Slider(Widget):
    def __init__(self, position, size=None, range=1):
        super(Slider, self).__init__(position, size)
        if not isinstance(range, list):
            range = [0, range-1]
        self.range = range
        if self.size is None:
            self.size = [max(self.range[1] * 20 + 20, 100), 20]

    def core(self):
        super(Slider, self).core()
        View.f.write(f"""
w{self.idx}.append('input')
    .attr('type', 'range')
    .attr('min', {self.range[0]})
    .attr('max', {self.range[1]})
    .attr('value', 0)
    .classed('slider', true)
    .attr('id', 'w{self.idx}')
    .style('width', '100%')
    .style('height', '100%')
    .on('input', e => {{
        const value = document.getElementById('w{self.idx}').value;
        d3.json(`/click/{self.idx}?value=${{value}}`).then(r => {{
            for(let i of r) triggers[i].dispatch('click');
        }});
    }});
w{self.idx}.append('button')
    .text('Play')
    .style('position', 'absolute')
    .style('width', '40px')
    .style('height', '21px')
    .style('left', '{self.size[0]+10}px')
    .style('top', '1.5px')
    .on('click', e => {{
        const s = document.getElementById('w{self.idx}');
        let i = {self.range[0]};
        let intervalId = setInterval(() => {{
            s.value = i;
            d3.select(s).dispatch('input');
            i++;
            if(i > {self.range[1]}) clearInterval(intervalId);
        }}, 800);
    }});
        """)


class Input(Widget):
    def __init__(self, position, size, text=''):
        super(Input, self).__init__(position, size)
        self.text = text

    def core(self):
        super(Input, self).core()
        View.f.write(f"""
w{self.idx}.append('input')
    .attr('type', 'text')
    .attr('value', '')
    .attr('id', 'w{self.idx}')
    .style('width', '100%')
    .style('height', '100%')
    .on('change', e => {{
        const value = document.getElementById('w{self.idx}').value;
        d3.json(`/click/{self.idx}?value=${{value}}`).then(r => {{
            for(let i of r) triggers[i].dispatch('click');
        }});
    }});
w{self.idx}.append('p')
    .text('lr:')
    .style('position', 'absolute')
    .style('width', '20px')
    .style('height', '20px')
    .style('left', '-20px')
    .style('top', '-15px');
d2.selectAll('input#w{self.idx}').attr('value', '{self.text}').dispatch('change');
        """)

    def click(self, request_args):
        value = request_args.get('value')
        if is_decimal(value):
            value = float(value)
        View.update_list.clear()
        self.click_(value)
        return json.dumps(View.update_list)


class Select(Widget):
    def __init__(self, position, size=(30, 30), options=None):
        super(Select, self).__init__(position, size)
        self.options = options

    def core(self):
        super(Select, self).core()
        View.f.write(f"""
const select{self.idx} = w{self.idx}.append('select').attr('id', 'w{self.idx}');
const options{self.idx} = {self.options};
select{self.idx}.selectAll('option')
    .data(options{self.idx})
    .enter()
    .append('option')
    .text(d => d);
select{self.idx}
    .on('change', e => {{
        const value = document.getElementById('w{self.idx}').selectedIndex;
        d3.json(`/click/{self.idx}?value=${{value}}`).then(r => {{
            for(let i of r) triggers[i].dispatch('click');
        }});;
    }});
        """)

    def click(self, request_args):
        value = int(request_args.get('value'))
        View.update_list.clear()
        self.click_(value)
        return json.dumps(View.update_list)


class Button(Widget):
    def __init__(self, position, size=(20, 10), text=''):
        super(Button, self).__init__(position, size)
        self.text = text

    def core(self):
        super(Button, self).core()
        View.f.write(f"""
    w{self.idx}.append('button')
        .text('{self.text}')
        .style('width', '100%')
        .style('height', '100%')
        .on('click', e => {{
            d3.json(`/click/{self.idx}?value={self.text}`).then(r => {{
                for(let i of r) triggers[i].dispatch('click');
            }});
        }});
            """)
