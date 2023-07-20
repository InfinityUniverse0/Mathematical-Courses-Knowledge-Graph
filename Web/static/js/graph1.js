// const btn1 = document.getElementById("all_course");
// btn1.addEventListener("click", graphDisplay);
var raw_nodes = document.currentScript.getAttribute('data-nodes');
var data_nodes = JSON.parse(raw_nodes);
var raw_links = document.currentScript.getAttribute('data-links');
var data_links = JSON.parse(raw_links);
//绘出知识图谱
let marge = { top: 0, bottom: 0, left: 0, right: 0 }
let svg = d3.select('svg')
let width = svg.attr('width')
let height = svg.attr('height')
// 先清除之前所绘制的图形，随后重新绘制
svg.selectAll("*").remove();
svg.call(
    d3.zoom().on('zoom', function () {
        g.attr('transform', d3.event.transform)
    })
)
    .on('dblclick.zoom', null)
let g = svg.append('g')
    .attr('transform', 'translate(' + marge.top + ',' + marge.left + ')')
    .attr('class', 'container')


// 准备数据
// 节点集
let nodes = data_nodes
// 边集
console.log(nodes)
let tempEdges = data_links
// 生成 nodes map
let nodesMap = genNodesMap(nodes);
console.log(nodesMap)
nodesData = d3.values(nodesMap)
let linkMap = genLinkMap(tempEdges)
// 构建 links（source 属性必须从 0 开始）
edges = genLinks(tempEdges);
// 设置一个颜色比例尺
let colorScale = d3.scaleOrdinal()
    .domain(d3.range(nodesData.length))
    .range(d3.schemeCategory10)
// 新建一个力导向图
let forceSimulation = d3.forceSimulation()
    .force('link', d3.forceLink())
    .force('charge', d3.forceManyBody())
    .force('center', d3.forceCenter())
// 生成节点数据
forceSimulation.nodes(nodesData)
// 生成边数据
forceSimulation.force('link')
    .links(edges)
    .distance(function (d) { // 每一边的长度
        return d.value * 200
    })
// 设置图形中心位置
forceSimulation.force('center')
    .x(width / 2)
    .y(height / 2)
// 箭头
var marker = g.append('g').attr('class', 'showLine').append('marker')
    .attr('id', 'resolved')
    // .attr("markerUnits","strokeWidth")// 设置为strokeWidth箭头会随着线的粗细发生变化
    .attr('markerUnits', 'userSpaceOnUse')
    .attr('viewBox', '0 -5 10 10')// 坐标系的区域
    .attr('refX', 44)// 箭头坐标
    .attr('refY', 0)
    .attr('markerWidth', 10)// 标识的大小
    .attr('markerHeight', 10)
    .attr('orient', 'auto')// 绘制方向，可设定为：auto（自动确认方向）和 角度值
    .attr('stroke-width', 2)// 箭头宽度
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')// 箭头的路径
    .attr('fill', '#000000')// 箭头颜色
// 绘制边
let links = g.append('g').selectAll('path')
    .data(edges)
    .enter()
    .append('path')
    .attr('d', link => genLinkPath(link)) // 遍历所有数据。d表示当前遍历到的数据，返回绘制的贝塞尔曲线
    .attr('id', (d, i) => { return 'edgepath' + d.id }) // 设置id，用于连线文字
    .style('stroke', '#000') // 线条颜色
    .style('stroke-width', 2) // 粗细
    .attr('class', 'lines')
    .attr('marker-end', 'url(#resolved)') // 根据箭头标记的id号标记箭头
// 边上的文字
let linksText = g.append('g')
    .selectAll('text')
    .data(edges)
    .enter()
    .append('text')
    .attr('class', 'linksText')
    .text(function (d) {
        return d.relations
    })
    .style('font-size', 14)
    .attr('fill-opacity', 0)
// 创建结点分组，用于绘图
let gs = g.append('g')
    .selectAll('.circleText')
    .data(nodesData)//
    .enter()
    .append('g')
    .attr('class', 'singleNode')
    .attr('id', function (d) {
        return 'singleNode' + d.id
    })
    .style('cursor', 'pointer')
    .attr('transform', function (d) {
        let cirX = d.x
        let cirY = d.y
        return 'translate(' + cirX + ',' + cirY + ')'
    })
// 鼠标交互

gs.on('mouseover', function (d, i) {
    // 显示连接线上的文字
    toggleLineText(d, true)
    toggleLine(links, d, true)
    toggleNode(gs, d, true)
})
    .on('mouseout', function (d, i) {
        // 隐去连接线上的文字
        toggleLineText(d, false)
        toggleLine(links, d, false)
        toggleNode(gs, d, false)
    })
    .on('click', function (d, i) {
        update_data(d.name)
        linksText.style('fill-opacity', function (edge) {
            if (edge.source === d) {
                return 1
            }
        })
        toggleCircle(d3.select(this), d)
    }, true)
    .call(d3.drag()
        .on('start', started)
        .on('drag', dragged)
        .on('end', ended)
    )
svg.on('click', function () {
    nodes.forEach(d => d.clickFlag = false)
    var event = d3.event
    var target = event.srcElement,   //  获取事件发生源
        data = d3.select(target).datum(); //  获取事件发生源的数据
    removeSingle()
    if (!data) {
        // document.getElementById('xxx').innerText = ''
    }
}, true)
forceSimulation.on('tick', ticked)

gs.append('circle')
    .attr('r', 35)
    .attr('id', function (d) {
        return 'circle' + d.id
    })
    .attr('fill', function (d, i) {
        //为不同层级的结点绘制不同的颜色
        if (d.level === 0) {
            // return '#FF3333';
            return '#00EE76';
        } else if (d.level === 1) {
            return '#00FFFF';
            // return '#F0FFF0';
        } else if (d.level === 2) {
            // return '#33FF33';
            return 'pink';
        } else {
            // return '#FFB7DD';
            return '#B0E2FF';
        }
    })
    .attr('stroke', 'grey')
    .attr('stroke-width', 3)
// 文字
var nodeText = gs.append('text')
    // .attr('x', -10)
    .attr('y', -20)
    .attr('dy', 10)
    .attr('text-anchor', 'middle')
    .style('font-size', 12)
    .attr('x', function ({ name }) {
        return textBreaking(d3.select(this), name)
    })
gs.append('title')
    .text((node) => {
        return node.name
    })

//更新结点和边数据
function updateData() {
    links = links
        .data(edges, function (d) {
        })
        .join("path")
        .attr('id', (d, i) => { return 'edgepath' + d.id }) // 设置id，用于连线文字
        .style('stroke', '#000') // 颜色
        .style('stroke-width', 2) // 粗细
        .attr('class', 'lines')
        .attr('marker-end', 'url(#resolved)') // 根据箭头标记的id号标记箭头
        .merge(links);
    linksText = linksText
        .data(edges)
        .join('text')
        .attr('class', 'linksText')
        .text(function (d) {
            return d.relations
        })
        .style('font-size', 14)
        .attr('fill-opacity', 0)
    gs = gs
        .data(nodesData, function (d) {
        })
        .join("g")
        .attr('class', 'singleNode')
        .attr('id', function (d) {
            return 'singleNode' + d.id
        })
        .style('cursor', 'pointer')
        .merge(gs)
        .call(d3.drag()
            .on("start", started)
            .on("drag", dragged)
            .on("end", ended));
    gs.append('circle')
        .attr('fill', function (d) {
            //为不同层级的结点绘制不同的颜色
            if (d.level === 0) {
                return '#00EE76';
            } else if (d.level === 1) {
                return '#F0FFF0';
            } else if (d.level === 2) {
                return 'pink';
            } else {
                return '#B0E2FF';
            }
        })
        .attr('r', 35)
        .attr('stroke', 'grey')
        .attr('stroke-width', 3)
    //鼠标移到结点时的操作
    gs.on('mouseover', function (d, i) {
        // 显示连接线上的文字
        toggleLineText(d, true)
        toggleLine(links, d, true)
        toggleNode(gs, d, true)
    })//鼠标移开结点时的操作
        .on('mouseout', function (d, i) {
            // 隐去连接线上的文字
            toggleLineText(d, false)
            toggleLine(links, d, false)
            toggleNode(gs, d, false)
        })//鼠标点击结点时操作
        .on('click', function (d, i) {
            linksText.style('fill-opacity', function (edge) {
                if (edge.source === d) {
                    return 1
                }
            })
            toggleCircle(d3.select(this), d)
        }, true)
    gs.append('text')
        .attr('y', -20)
        .attr('dy', 10)
        .attr('text-anchor', 'middle')
        .style('font-size', 12)
        .attr('x', function ({ name }) {
            return textBreaking(d3.select(this), name)
        })
    gs.append('title')
        .text((node) => {
            return node.name
        })
    forceSimulation.nodes(nodesData);
    forceSimulation.force("link").links(edges);
    forceSimulation.alpha(0.8).restart();
}

function getLineTextAngle(d, bbox) {
    if (d.target.x < d.source.x) {
        const {
            x,
            y,
            width,
            height
        } = bbox;
        const rx = x + width / 2;
        const ry = y + height / 2;
        return 'rotate(180 ' + rx + ' ' + ry + ')';
    } else {
        return 'rotate(0)';
    }
}

function toggleNode(nodeCircle, currNode, isHover) {
    if (isHover) {
        // 提升节点层级
        // nodeCircle.sort((a, b) => a.id === currNode.id ? 1 : -1);
        // this.parentNode.appendChild(this);
        nodeCircle
            .style('opacity', .1)
            .filter(node => isLinkNode(currNode, node))
            .style('opacity', 1);

    } else {
        nodeCircle.style('opacity', 1);
    }

}

function removeSingle() {
    d3.select('.singleCircle').remove()
}

function toggleCircle(current, d) {
    var currentD = d
    if (d.clickFlag) {
        removeSingle()
        // document.getElementById('xxx').innerText = ''
    }
    d.clickFlag = true
    // document.getElementById('xxx').innerText = d.name
    var data = [{
        population: 30,
        value: 'X',
        type: 'delete'
    }, {
        population: 30,
        value: '收起',
        type: 'showOff'
    }, {
        population: 30,
        value: '查看详细信息',
        type: 'showDetail'
    }]
    var sum = d3.sum(data.map(function (d) {
        return d.population
    }))
    for (i in data) {
        data[i].Percentage = (data[i].population / sum * 100).toFixed(0) + "%";
    }
    var width = 300,
        height = 300,
        margin = { "left": 30, "top": 30, "right": 30, "bottom": 30 },
        svg_width = width + margin.left + margin.right,
        svg_height = height + margin.top + margin.bottom,
        font_size = 15;
    var g = current
        .append("g")
        .attr('class', 'singleCircle')
        .attr("width", width)
        .attr("height", height)
    var Pie = g.append("g")

    var arc_generator = d3.arc()
        .innerRadius(width / 6.5)
        .outerRadius(width / 4)
    var angle_data = d3.pie()
        .value(function (d) {
            return d.population;
        })
    var pieData = angle_data(data)
    var pieAngle = pieData.map(function (p) {
        return (p.startAngle + p.endAngle) / 2 / Math.PI * 180;
    });

    // var color=d3.schemeCategory10;

    //生成内部圆环
    Pie.selectAll("path")
        .data(angle_data(data))
        .enter()
        .append("path")
        .attr("d", arc_generator)
        .style("fill", function (d, i) {
            return 'gray';//结点环颜色
        })
        .style('stroke', 'black')
        .attr("class", "path")
        .attr('type', function (d) {
            return d.data.type
        })
        .on('click', function (d) {
            if (d.data.type === 'delete') {
                deleteNode(currentD)
            } else if (d.data.type === 'showOn') {
                deleteNextNodes(currentD)
            } else {
                // showMyList()

            }
            d3.event.stopPropagation()
        })
    var arc_label = d3.arc()
        .innerRadius(width / 4)
        .outerRadius(width / 2)

    Pie.selectAll(".arc_label")
        .data(angle_data(data))
        .enter()
        .append("path")
        .attr("d", arc_label)
        .attr("class", "arc_label")
        .style("fill", "none")
    const labelFontSize = 12;
    const labelValRadius = (170 * 0.35 - labelFontSize * 0.35); // 计算正确半径 文字位置
    const labelValRadius1 = (170 * 0.35 + labelFontSize * 0.35);


    const labelsVals = current.select('.singleCircle').append('g')
        .classed('labelsvals', true);

    // 定义两条路径以使标签的方向正确
    labelsVals.append('def')
        .append('path')
        .attr('id', 'label-path-1')
        .attr('d', `m0 ${-labelValRadius} a${labelValRadius} ${labelValRadius} 0 1,1 -0.01 0`);
    labelsVals.append('def')
        .append('path')
        .attr('id', 'label-path-2')
        .attr('d', `m0 ${-labelValRadius1} a${labelValRadius1} ${labelValRadius1} 0 1,0 0.01 0`);

    labelsVals.selectAll('text')
        .data(data)
        .enter()
        .append('text')
        .style('font-size', labelFontSize)
        .style('fill', 'black')
        .style('font-weight', "bold")
        .style('text-anchor', 'middle')
        .append('textPath')
        .attr('href', function (d, i) {
            const p = pieData[i];
            const angle = pieAngle[i];
            if (angle > 90 && angle <= 270) { // 根据角度选择路径
                return '#label-path-2';
            } else {
                return '#label-path-1';
            }
        })
        .attr('startOffset', function (d, i) {
            const p = pieData[i];
            const angle = pieAngle[i];
            let percent = (p.startAngle + p.endAngle) / 2 / 2 / Math.PI * 100;
            if (angle > 90 && angle <= 270) { // 分别计算每条路径的正确百分比
                return 100 - percent + "%";
            }
            return percent + "%";
        })
        .text(function (d) {
            return d.value;
        })
        .on('click', function (d) {
            if (d.type === 'delete') {
                deleteNode(currentD)
            } else if (d.type === 'showOff') {
                deleteNextNodes(currentD)
            } else {
                // showMyList()

            }
            d3.event.stopPropagation()
        }, true)
}

function deleteNextNodes(curr) {
    // document.getElementById('xxx').innerText = '';
    // var removeIndex = nodesData.findIndex(node=>node.id == curr.id)
    // nodesData.splice(removeIndex,1)
    // nodes.splice(removeIndex,1)
    d3.select(this).remove();
    let relationNode = [],
        relationList = [],
        hasRelationList = []
    var clickNode = curr.id;//点击节点的名字
    d3.selectAll(".lines").each(function (e) {
        if (e.source.id == curr.id || e.target.id == curr.id) {
            hasRelationList.push(e)
        } else {
            relationList.push(e)//出去跟删除节点有关系的其他关系
        }
        //需要删除的节点相关的节点
        if (e.source.id == curr.id) {
            relationNode.push(e.target)
        }
        //需要删除的节点相关的节点
        if (e.target.id == curr.id) {
            relationNode.push(e.source)
        }
    })
    var tempNodeList = JSON.parse(JSON.stringify(relationNode))
    tempNodeList = uniqObjInArray(tempNodeList)
    //区分下级节点是否是孤节点
    tempNodeList.forEach(function (item, index) {
        var hasLine = relationList.findIndex(jtem => jtem.target.id == item.id || jtem.source.id == item.id)
        if (hasLine >= 0) {
            item.notSingle = true
        }
    })
    tempNodeList.forEach(function (item, index) {
        if (!item.notSingle) {
            d3.select('#singleNode' + item.id).remove()
        }
    })
    var otherTempNode = [];
    tempNodeList = tempNodeList.map(item => {
        if (!item.notSingle) {
            otherTempNode.push(item)
        }
    })
    hasRelationList.forEach(item => {
        otherTempNode.forEach(jtem => {
            if (jtem.id == item.source.id || jtem.id == item.target.id) {
                d3.select('#edgepath' + item.id).remove()
            }
        })
    })
    d3.selectAll(".singleNode").each(function (d, i) {
        var temp = d.id;
        //删除当前需要隐藏的节点
        if (temp == clickNode) {
            removeSingle()
        }
    });
    d3.selectAll(".linksText").each(function (e) {
        if (e.source === curr || e.target === curr) {
            d3.select(this).remove();
        }
    })
    gs.style('opacity', 1);
    links.style('opacity', 1)
        .classed('link-active', false);
}

function deleteNode(curr) {
    document.getElementById('xxx').innerText = '';
    var removeIndex = nodesData.findIndex(node => node.id == curr.id)
    nodesData.splice(removeIndex, 1)
    nodes.splice(removeIndex, 1)
    d3.select(this).remove();
    let relationNode = [],
        relationList = []
    var clickNode = curr.id;//点击节点的名字
    d3.selectAll(".lines").each(function (e) {
        if (e.source.id == curr.id || e.target.id == curr.id) {
            d3.select(this).remove();
        } else {
            relationList.push(e)//出去跟删除节点有关系的其他关系
        }
        //需要删除的节点相关的节点
        if (e.source.id == curr.id) {
            relationNode.push(e.target)
        }
        //需要删除的节点相关的节点
        if (e.target.id == curr.id) {
            relationNode.push(e.source)
        }
    })
    var tempNodeList = JSON.parse(JSON.stringify(relationNode))
    tempNodeList = uniqObjInArray(tempNodeList)
    //区分下级节点是否是孤节点
    tempNodeList.forEach(function (item, index) {
        var hasLine = relationList.findIndex(jtem => jtem.target.id == item.id || jtem.source.id == item.id)
        if (hasLine >= 0) {
            item.notSingle = true
        }
    })
    tempNodeList.forEach(function (item, index) {
        if (!item.notSingle) {
            d3.select('#singleNode' + item.id).remove()
        }
    })
    d3.selectAll(".singleNode").each(function (d, i) {
        var temp = d.id;
        //删除当前需要隐藏的节点
        if (temp == clickNode) {
            removeSingle()
            d3.select(this).remove();
        }
    });
    d3.selectAll(".linksText").each(function (e) {
        if (e.source === curr || e.target === curr) {
            d3.select(this).remove();
        }
    })
    gs.style('opacity', 1);
    links.style('opacity', 1)
        .classed('link-active', false);
}

function uniqObjInArray(objarray) {
    let len = objarray.length;
    let tempJson = {

    };
    let res = [];
    for (let i = 0; i < len; i++) {
        //取出每一个对象
        tempJson[JSON.stringify(objarray[i])] = true;
    }
    let keyItems = Object.keys(tempJson);
    for (let j = 0; j < keyItems.length; j++) {
        res.push(JSON.parse(keyItems[j]));
    }
    return res;
}
function isLinkLine(node, link) {
    return link.source.id === node.id
}
function isLinkNode(currNode, node) {
    if (currNode.id === node.id) {
        return true;
    }
    return linkMap[currNode.id + '-' + node.id] || linkMap[node.id + '-' + currNode.id];
}
function largerNode(nodes, currNode, isHover) {
    if (isHover) {
        gs
            .style('stroke-width', 1)
            .filter(node => isNode(currNode, node))
            .style('stroke-width', 10)
    } else {
        gs
            .style('stroke-width', 1)
    }
}

function isNode(node, cNode) {
    return true
}

function genLinkMap(relations) {
    const hash = {};
    relations.map(function ({
        source,
        target,
        relation
    }) {
        const key = source + '-' + target;
        if (hash[key]) {
            hash[key] += 1;
            hash[key + '-relation'] += '、' + relation;
        } else {
            hash[key] = 1;
            hash[key + '-relation'] = relation;
        }
    });
    return hash;
}

function genLinks(relations) {
    const indexHash = {};
    return relations.map(function ({
        id,
        source,
        target,
        relation,
        value
    }, i) {
        const linkKey = source + '-' + target;
        const count = linkMap[linkKey];
        if (indexHash[linkKey]) {
            indexHash[linkKey] -= 1;
        } else {
            indexHash[linkKey] = count - 1;
        }
        return {
            id,
            source: nodesMap[source],
            target: nodesMap[target],
            relation,
            value,
            relations: linkMap[linkKey + '-relation'],
            count: linkMap[linkKey],
            index: indexHash[linkKey]
        }
    })
}

function genLinkPath(link) {
    const count = link.count;
    const index = link.index;
    let sx = link.source.x;
    let tx = link.target.x;
    let sy = link.source.y;
    let ty = link.target.y;
    return 'M' + sx + ',' + sy + ' L' + tx + ',' + ty;
}

function genNodesMap(nodes) {
    const hash = {};
    nodes.map(function ({
        id,
        name,
        level
    }) {
        hash[id] = {
            id,
            name,
            level
        };
    });
    return hash;
}

function textBreaking(d3text, text) {
    const len = text.length
    if (len <= 3) {
        d3text.append('tspan')
            .attr('x', 0)
            .attr('y', -3)
            .text(text)
    } else {
        const topText = text.substring(0, 3)
        const midText = text.substring(3, 7)
        let botText = text.substring(7, len)
        let topY = -22
        let midY = 8
        let botY = 34
        if (len <= 9) {
            topY += 10
            midY += 10
        } else {
            botText = text.substring(7, 9) + '...'
        }
        d3text.text('')
        d3text.append('tspan')
            .attr('x', 0)
            .attr('y', topY)
            .text(function () {
                return topText
            })
        d3text.append('tspan')
            .attr('x', 0)
            .attr('y', midY)
            .text(function () {
                return midText
            })
        d3text.append('tspan')
            .attr('x', 0)
            .attr('y', botY - 7)
            .text(function () {
                return botText
            })
    }
}

function ticked() {
    // 连线路径
    links
        .attr('d', link => genLinkPath(link))
    // 连线文字位置
    linksText
        .attr('x', function (d) { return (d.source.x + d.target.x) / 2 })
        .attr('y', function (d) { return (d.source.y + d.target.y) / 2 })
    // 节点位置
    gs
        .attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')' })
}

function started(d) {
    if (!d3.event.active) {
        forceSimulation.alphaTarget(0.8).restart() // 设置衰减系数，对节点位置移动过程的模拟，数值越高移动越快，数值范围[0, 1]
    }
    d.fx = d.x
    d.fy = d.y
}

function dragged(d) {
    d.fx = d3.event.x
    d.fy = d3.event.y
}

function ended(d) {
    if (!d3.event.active) {
        forceSimulation.alphaTarget(0)
    }
    d.fx = null
    d.fy = null
}

function showMyList() {
    var e = { id: 10, name: "河北" };
    var h = { id: 11, name: "河南" };
    var f = { id: 13, source: 9, target: 10, relation: '222', value: 2 };
    nodes.push(e);
    nodes.push(h);
    tempEdges.push(f);
    nodesMap = genNodesMap(nodes);
    nodesData = d3.values(nodesMap)
    linkMap = genLinkMap(tempEdges)
    edges = genLinks(tempEdges)
    updateData()
}

function toggleLine(linkLine, currNode, isHover) {
    if (isHover) {
        // 加重连线样式
        links
            .style('opacity', 0.1)
            .filter(link => isLinkLine(currNode, link))
            .style('opacity', 1)
            .classed('link-active', true)
    } else {
        links
            .style('opacity', 1)
            .classed('link-active', false)
    }
}

function toggleLineText(currNode, isHover) {
    if (isHover) {
        linksText.style('fill-opacity', function (edge) {
            if (edge.source === currNode) {
                return 1
            }
        })
    } else {
        linksText.style('fill-opacity', function (edge) {
            if (edge.source === currNode || edge.target === currNode) {
                return 0
            }
        })
    }
}
