import data from './out3.js'

console.log(data);

const myChart = echarts.init(document.getElementById('graph'));

let option = {
  title: {
    text: 'Aesthetics Wiki Pages'
  },
  series: [
    {
      type: 'graph',
      nodes: data.nodes,
      links: data.links,
      roam: true,
      lineStyle: {
        opacity: 0.2,
        width: 0.5
      },
      focusNodeAdjacency: true,
      emphasis: {
        label: {
          show: true,
          position: 'inside',
          fontSize: 16,
          color: '#fff'
        },
        lineStyle: {
          opacity: 0.5,
          width: 0.7
        },
      },
      symbolSize: 5
    }
  ]
};

myChart.setOption(option);
