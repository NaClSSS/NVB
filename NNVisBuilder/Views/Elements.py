from backend import Container
from . import View
import numpy as np
from NNVisBuilder.GlobalVariables import *


class Element:
    def __init__(self, gid, data=None, ele_id=-1, reg_no=-1, ms=None, **info):
        """
        self.gid: int, id of view
        self.ele_id: str, id to distinguish element
        """
        self.gid = gid
        self.ele_id = 'c%d' % gid
        if ele_id != -1:
            self.ele_id = 'c%d_%d' % (gid, ele_id)
        self.data = data
        self.reg_no = reg_no
        self.ms = ms
        self.merge_r = View.merge_r if self.ms is None else self.ms.merge_r
        self.info = info
        self.selectors = self.init_selectors()
        if self.ms is not None:
            self.ms.set_selectors(self.selectors)
        Container.click_handler[self.ele_id] = self.default_click
        Container.brush_handler[self.ele_id] = self.brush_

    def core(self, views=None):
        return ''

    def default_click(self, info):
        return View.idm.empty_r()

    def init_selectors(self):
        return []

    def brush_(self, info):
        return View.idm.empty_r()

    def on_click(self, f):
        if f is None:
            def f(info):
                return View.idm.empty_r()
        Container.click_handler[self.ele_id] = f

    def on_brush(self, f):
        if f is None:
            def f(info):
                return View.idm.empty_r()
        Container.brush_handler[self.ele_id] = f

    def response(self, back=False, views=None):
        return ''


class Circle(Element):
    def core(self, views=None):
        return f"""
const data{self.ele_id} = {self.data[['x', 'y', 'r', 'color', 'opacity', 'idx']].to_json(orient='records')};
g{self.gid}.selectAll('circle.{self.ele_id}')
    .data(data{self.ele_id})
    .enter()
    .append('circle')
    .classed('{self.ele_id}', true)
    .attr('r', d => d.r)
    .attr('cx', d => sx{self.ele_id}(d.x))
    .attr('cy', d => sy{self.ele_id}(d.y)) 
    .attr('fill', d => d.color)
    .attr('opacity', d => d.opacity)
    .on('click', e => {{
        const idx = {select_this}.datum().idx;
        d3.json(`/click/{self.ele_id}?idx=${{idx}}`).then(r => {{
            {newline.join([view.response(views) for view in views])}
        }});
    }});
        """.strip() + "\n"

    def brush(self):
        return f"""
g{self.gid}.selectAll("circle.{self.ele_id}")
    .each(d => {{
        const cx = sx{self.ele_id}(d.x), cy = sy{self.ele_id}(d.y), pos = brush_ids.indexOf(d.idx);
        if (cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1) {{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else if(pos != -1) brush_ids.splice(pos, 1);
    }});  
//d3.json for response
r = brush_ids;
        """.strip() + "\n"

    def init_selectors(self):
        return {
            'in_box': f"""
g{self.gid}.selectAll("circle.{self.ele_id}")
    .each(d => {{
        const cx = sx{self.ele_id}(d.x), cy = sy{self.ele_id}(d.y), pos = brush_ids.indexOf(d.idx);
        if (cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1) {{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else if(pos != -1) brush_ids.splice(pos, 1);
    }});""",
            'out_box': f"""
g{self.gid}.selectAll("circle.{self.ele_id}")
    .each(d => {{
        const cx = sx{self.ele_id}(d.x), cy = sy{self.ele_id}(d.y), pos = brush_ids.indexOf(d.idx);
        if (cx < x0 || cx > x1 || cy < y0 || cy > y1) {{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else if(pos != -1) brush_ids.splice(pos, 1);
    }});""",
            'left_box': f"""
g{self.gid}.selectAll("circle.{self.ele_id}")
    .each(d => {{
        const cx = sx{self.ele_id}(d.x), cy = sy{self.ele_id}(d.y), pos = brush_ids.indexOf(d.idx);
        if (cx < x0) {{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else if(pos != -1) brush_ids.splice(pos, 1);
    }});""",
            'right_box': f"""
g{self.gid}.selectAll("circle.{self.ele_id}")
    .each(d => {{
        const cx = sx{self.ele_id}(d.x), cy = sy{self.ele_id}(d.y), pos = brush_ids.indexOf(d.idx);
        if (cx > x0) {{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else if(pos != -1) brush_ids.splice(pos, 1);
    }});""",
            'up_box': f"""
g{self.gid}.selectAll("circle.{self.ele_id}")
    .each(d => {{
        const cx = sx{self.ele_id}(d.x), cy = sy{self.ele_id}(d.y), pos = brush_ids.indexOf(d.idx);
        if (cy < y0) {{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else if(pos != -1) brush_ids.splice(pos, 1);
    }});""",
            'down_box': f"""
g{self.gid}.selectAll("circle.{self.ele_id}")
    .each(d => {{
        const cx = sx{self.ele_id}(d.x), cy = sy{self.ele_id}(d.y), pos = brush_ids.indexOf(d.idx);
        if (cy > y1) {{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else if(pos != -1) brush_ids.splice(pos, 1);
    }});"""
        }

    def default_click(self, info):
        idx = int(info.get('idx'))
        r = {}
        if View.click_mode == 0:
            label = self.data[self.data.idx == idx].label.values[0]
            r[self.reg_no] = self.data[self.data.label == label].gid.values.tolist()
        elif View.click_mode == 1:
            embedding = np.array(self.data[self.data.idx == idx].embedding.values[0])
            embeddings = np.stack(self.data['embedding'])
            temp = self.data.idx.to_frame()
            temp['dist'] = np.linalg.norm(embeddings - embedding, axis=1)
            temp = temp.sort_values(by='dist')
            num = info.get('num', 32)
            r[self.reg_no] = temp.iloc[:num].idx.values.tolist()
        for reg_no in View.idm.get_all_reg_no():
            if reg_no == self.reg_no:
                continue
            r[reg_no] = View.idm.map(self.reg_no, reg_no, r[self.reg_no])
        return r

    # brush是选出哪些元素，brush_是如何进一步映射到所有id，brush_后面换个名字
    def brush_(self, info):
        ids = info.get('ids')
        r = View.idm.empty_r()
        if ids == '':
            return self.merge_r(r)
        ids = [int(x) for x in ids.split(',')]
        for reg_no in View.idm.get_all_reg_no():
            if reg_no == self.reg_no:
                r[self.reg_no] = ids
            else:
                r[reg_no] = View.idm.map(self.reg_no, reg_no, r[self.reg_no])
        return self.merge_r(r)

    def response(self, back=False, views=None):
        if back:
            return f"""
g{self.gid}.selectAll("circle.{self.ele_id}")
    .attr('fill', d => {{
        if(r_[{self.reg_no}].indexOf(d.idx) != -1){{
            if(selected_back[{self.reg_no}].indexOf(d.idx) != -1) return 'red';
            else return 'aqua';
        }}
        return d.color;
    }});
            """
        else:
            return f"""
            if(typeof(r[{self.reg_no}]) != 'undefined'){{
                g{self.gid}.selectAll("circle.{self.ele_id}")
                    .attr('fill', d => {{
                        if(r[{self.reg_no}].indexOf(d.idx) != -1) return 'aqua';
                        return d.color;
                    }});
            }}
                        """.strip() + "\n"
#             return f"""
# g{self.idx}.selectAll("circle.{self.ele_id}")
#     .attr('r', (d, i) => {{
#         if(selected[{self.reg_no}].indexOf(i) != -1) return 1.6 * d.point_size;
#         return d.point_size;
#     }});
#             """.strip() + "\n"


class Rect(Element):
    def core(self, views=None):
        """
        data: list of (x, y, width, height, color)
        x & y may need scale, width & height never need.
        """
        w = self.ele_id if self.info.get('use_ls', True) else self.gid
        return f"""
const data{self.ele_id} = {self.data[['x', 'y', 'width', 'height', 'color', 'idx']].to_json(orient='records')};
g{self.gid}.selectAll("rect.{self.ele_id}")
    .data(data{self.ele_id})
    .enter()
    .append("rect")
    .classed('{self.ele_id}', true)
    .attr('x', d => sx{w}(d.x))
    .attr('y', d => sy{w}(d.y))
    .attr('width', d => d.width)
    .attr('height', d => d.height)
    .attr('fill', d => d.color)
    .on('click', e => {{
        const idx = {select_this}.datum().idx;
        d3.json(`/click/{self.ele_id}?idx=${{idx}}`).then(r => {{
            {newline.join([view.response(views) for view in views])}
        }});
    }});
        """.strip() + "\n"

    def default_click(self, info):
        idx = int(info.get('idx'))
        r = {self.reg_no: [idx]}
        for reg_no in View.idm.get_all_reg_no():
            if reg_no == self.reg_no:
                continue
            r[reg_no] = View.idm.map(self.reg_no, reg_no, r[self.reg_no])
        return r

    def response(self, back=False, views=None):
        if back:
            return ''
        else:
            return f"""
        g{self.gid}.selectAll("rect.{self.ele_id}")
            .attr('fill', d => {{
                if(r[{self.reg_no}].indexOf(d.idx) != -1) return 'red';
                return d.color;
            }});
                    """.strip() + "\n"


class Path(Element):
    def __init__(self, idx, data=None, ele_id=-1, reg_no=-1, ms=None, **info):
        super(Path, self).__init__(idx, data, ele_id, reg_no, ms, **info)
        self.threshold = 0

    def core(self, views=None):
        w = self.ele_id if self.info.get('use_ls', True) else self.gid
        return f"""
const line{self.ele_id} = d3.line();
const data{self.ele_id} = {self.data[['idx', 'path', 'color']].to_json(orient='records')};
g{self.gid}.selectAll('path.{self.ele_id}')
    .data(data{self.ele_id})
    .enter()
    .append('path')
    .classed('{self.ele_id}', true)
    .attr('d', d => line{self.ele_id}(d.path.map(v => [sx{w}(v[0]), sy{w}(v[1])])))
    .attr('stroke', d => d.color)
    .attr('fill', 'none')
    .attr('opacity', 0.6);
            """.strip() + "\n"

    def brush(self):
        w = self.ele_id if self.info.get('use_ls', True) else self.gid
        # 这一部分在选中的同时response了啊手动阀苦涩JFK垃圾啊士大夫
        return f"""
g{self.gid}.selectAll('path.{self.ele_id}')
    .each(d => {{
        const temp = d.path;
        let flag = true, flag1 = false;
        for(let i=0;i<temp.length;i++){{
            if(sx{w}(temp[i][0])>=x0 && sx{w}(temp[i][0])<=x1 && (temp[i][1])>=r) flag1 = true;
            if(sx{w}(temp[i][0])>=x0 && sx{w}(temp[i][0])<=x1 && (temp[i][1])<r) flag = false;
        }}
        pos = brush_ids.indexOf(d.idx);
        if(flag && flag1){{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else{{
            if(pos != -1) brush_ids.splice(pos, 1);
        }}
    }});
            """.strip() + "\n"

    def init_selectors(self):
        w = self.ele_id if self.info.get('use_ls', True) else self.gid
        return {
            'in_box': f"""
g{self.gid}.selectAll('path.{self.ele_id}')
    .each(d => {{
        const temp = d.path;
        let flag = false, flag1 = true;
        for(let i=0;i<temp.length;i++){{
            if(sx{w}(temp[i][0])>=x0 && sx{w}(temp[i][0])<=x1){{
                flag = true;
                if(sy{w}(temp[i][1])>y1 || sy{w}(temp[i][1])<y0){{
                    flag1 = false;
                    break;
                }}
            }}
        }}
        pos = brush_ids.indexOf(d.idx);
        if(flag && flag1){{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else{{
            if(pos != -1) brush_ids.splice(pos, 1);
        }}
    }});
        """,
            'down_box': f"""
g{self.gid}.selectAll('path.{self.ele_id}')
    .each(d => {{
        const temp = d.path;
        let flag = false, flag1 = true;
        for(let i=0;i<temp.length;i++){{
            if(sx{w}(temp[i][0])>=x0 && sx{w}(temp[i][0])<=x1){{
                flag = true;
                if(sy{w}(temp[i][1]) < y1){{
                    flag1 = false;
                    break;
                }}
            }}
        }}
        pos = brush_ids.indexOf(d.idx);
        if(flag && flag1){{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else{{
            if(pos != -1) brush_ids.splice(pos, 1);
        }}
    }});
        """,
            'up_box': f"""
g{self.gid}.selectAll('path.{self.ele_id}')
    .each(d => {{
        const temp = d.path;
        let flag = false, flag1 = true;
        for(let i=0;i<temp.length;i++){{
            if(sx{w}(temp[i][0])>=x0 && sx{w}(temp[i][0])<=x1){{
                flag = true;
                if(sy{w}(temp[i][1]) > y0){{
                    flag1 = false;
                    break;
                }}
            }}
        }}
        pos = brush_ids.indexOf(d.idx);
        if(flag && flag1){{
            if(pos == -1) brush_ids.push(d.idx);
        }}
        else{{
            if(pos != -1) brush_ids.splice(pos, 1);
        }}
    }});
        """
        }

    def brush_(self, info):
        ids = info.get('ids')
        threshold = float(info.get('threshold', self.threshold))
        r = View.idm.empty_r()
        if ids == '':
            return self.merge_r(r)
        ids = [int(x) for x in ids.split(',')]
        for reg_no in View.idm.get_all_reg_no():
            if reg_no == 0:
                embedding = self.info['embedding']
                a = np.zeros([embedding.shape[0], ], dtype=int)
                for i in range(embedding.shape[0]):
                    for j in ids:
                        if embedding[i, j] >= threshold:
                            a[i] += 1
                b = np.argsort(-a)
                r[reg_no] = b[:10].tolist()
                r[100] = a.tolist()
                r[101] = len(ids)
            elif reg_no == self.reg_no:
                r[self.reg_no] = ids
            else:
                r[reg_no] = []
        return self.merge_r(r)

    def set_threshold(self, threshold):
        self.threshold = threshold

    def response(self, back=False, views=None):
        if not back:
            w = self.ele_id if self.info.get('use_ls', True) else self.gid
            return f"""
    if(typeof(r['threshold']) != 'undefined'){{
        const line{self.ele_id} = d3.line();
        g{self.gid}.selectAll('path.{self.ele_id}').remove();
        g{self.gid}.selectAll('path.{self.ele_id}')
            .data(r['threshold'])
            .enter()
            .append('path')
            .classed('{self.ele_id}', true)
            .attr('d', d => line{self.ele_id}(d.path.map(v => [sx{w}(v[0]), sy{w}(v[1])])))
            .attr('stroke', d => d.color)
            .attr('fill', 'none');
    }}
    if(typeof(r[{self.reg_no}]) != 'undefined'){{
        if(true){{
            if(r[{self.reg_no}].length == 0){{
                g{self.gid}.selectAll('path.{self.ele_id}')
                    .attr('stroke', d => d.color)
                    .attr('stroke-width', 1)
                    .attr('opacity', 0.6);
            }}
            else{{
                g{self.gid}.selectAll('path.{self.ele_id}')
                    .attr('stroke', d => {{
                        const pos = r[{self.reg_no}].indexOf(d.idx);
                        if(pos != -1){{
                            return 'blue';
                        }}
                        else{{
                            return d.color;
                        }}
                    }});
            }}
        }}
        else{{
            if(r[{self.reg_no}].length == 0){{
                g{self.gid}.selectAll('path.{self.ele_id}')
                    .attr('stroke', d => d.color)
                    .attr('stroke-width', 1)
                    .attr('opacity', 0.6);
            }}
            else{{
                g{self.gid}.selectAll('path.{self.ele_id}')
                    .attr('stroke', d => {{
                        const pos = r[2000][{self.reg_no}].indexOf(d.idx), pos1 = r[{self.reg_no}].indexOf(d.idx);
                        if(pos1 != -1){{
                            return 'red';
                        }}
                        else if(pos != -1){{
                            return 'blue';
                        }}
                        else{{
                            return d.color;
                        }}
                    }});
                g{self.gid}.selectAll('path.{self.ele_id}')
                    .attr('opacity', d => {{
                        const pos = r[2000][{self.reg_no}].indexOf(d.idx), pos1 = r[{self.reg_no}].indexOf(d.idx);
                        if(pos1 != -1){{
                            return 1;
                        }}
                        else if(pos != -1){{
                            return 0.5;
                        }}
                        else{{
                            return 0.25;
                        }}
                    }});
                g{self.gid}.selectAll('path.{self.ele_id}')
                    .attr('stroke-width', d => {{
                        const pos = r[2000][{self.reg_no}].indexOf(d.idx), pos1 = r[{self.reg_no}].indexOf(d.idx);
                        if(pos1 != -1){{
                            return 3;
                        }}
                        else if(pos != -1){{
                            return 1.8;
                        }}
                        else{{
                            return 1;
                        }}
                    }});
            }}
        }}
    }}
            """
        else:
            return f"""
    if(typeof(selected_back[{self.reg_no}]) != 'undefined'){{
        g{self.gid}.selectAll('path.{self.ele_id}')
        .attr('stroke', d => {{
            let pos = brush_ids.indexOf(d.idx)
            if(pos == -1){{
                return d.color;
            }}
            else{{
                pos = selected_back[{self.reg_no}].indexOf(d.idx);
                if(pos == -1) return 'red';
                return 'blue';
            }}
        }});
    }}
            """


class Link(Element):
    def response(self, back=False, views=None):
        if back:
            return f"""
const link{self.ele_id} = d3.linkVertical();
const data{self.ele_id} = selected_back[{self.reg_no}]['element'];
g{self.gid}.selectAll('path.{self.ele_id}').remove();
g{self.gid}.selectAll('path.{self.ele_id}')
    .data(data{self.ele_id})
    .enter()
    .append('path')
    .classed('{self.ele_id}', true)
    .attr('d', d => link{self.ele_id}({{'source':[sx{self.ele_id}(d.ends.source[0]), sy{self.ele_id}(d.ends.source[1])], 
        'target':[sx{self.ele_id}(d.ends.target[0]), sy{self.ele_id}(d.ends.target[1])]}}))
    .attr('stroke', d => d.color)
    .attr('stroke-width', d => d.width>0.1?`${{d.width}}px`:'0.1px')
    .attr('fill', 'none');
                """.strip() + "\n"
        else:
            return ''


class TextRect(Element):
    def __init__(self, gid, data=None, ele_id=-1, reg_no=-1, vcs=(), **info):
        super(TextRect, self).__init__(gid, data, ele_id, reg_no, **info)
        self.vcs = vcs

    def response(self, back=False, views=None):
        if not back:
            return f"""
const data{self.ele_id} = r[{self.reg_no}];
//save r's info by new brush_ids
let brush_ids{self.ele_id} = data{self.ele_id};
g{self.gid}.selectAll('g').remove();
const gs{self.ele_id} = g{self.gid}.selectAll('g')
    .data(data{self.ele_id})
    .enter()
    .append('g')
    .attr('transform', `translate(${{rx{self.gid}}}, ${{ry{self.gid}}})`);
gs{self.ele_id}.append('rect')
    .attr('x', (d, i) => 50 * (i % 20))
    .attr('y', (d, i) => Math.floor(i / 20) * 15)
    .attr('width', 50)
    .attr('height', 15)
    .attr('fill', 'blue')
    .attr('stroke', 'purple')
    .attr('opacity', 0.3)
    .on('click', e => {{
        const t = {select_this}, d = t.datum(), pos = brush_ids{self.ele_id}.indexOf(d);
        if(t.attr('fill') == 'blue'){{
            t.attr('fill', 'red');
            if(pos != -1) brush_ids{self.ele_id}.splice(pos, 1);
        }}
        else{{
            t.attr('fill', 'blue');
            if(pos == -1) brush_ids{self.ele_id}.push(d);
        }}
        d3.json(`/brush/{self.info['plc'].elements.ele_id}?ids=${{brush_ids{self.ele_id}}}`).then(selected_back => {{
            {newline.join([view.response(views, back=True) for view in views if isinstance(view, self.vcs)])}
        }});
    }});
det = gs{self.ele_id};
gs{self.ele_id}.append('text')
    .text(d => d)
    .attr('x', (d, i) => 50 * (i % 20))
    .attr('y', (d, i) => Math.floor(i / 20) * 15)
    .attr('dx', 15)
    .attr('dy', 14)
    .attr('fill', 'black');
            """
        else:
            return ''
