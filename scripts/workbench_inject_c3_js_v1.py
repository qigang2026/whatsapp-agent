#!/usr/bin/env python3
"""
批次 6 步骤 2：把 AI 跟进概要-PC.html 的 CSS + JS 注入 WhatsApp-Agent-PC.html
- CSS 注入到 </style> 前
- JS（ECharts CDN + 4 个图表初始化）注入到 </body> 前
- 不重复注入（幂等检查）
"""

import re
from pathlib import Path

ROOT = Path('/Users/qigangye/Mstar/WhatsApp Agent')
TARGET = ROOT / 'WhatsApp-Agent-PC.html'

html = TARGET.read_text(encoding='utf-8')

# ========== 1. CSS 注入 ==========
# 在 AI 跟进概要中已知的相关 CSS 区块（从 .time-filter 到 .stage-chip）
CSS_BLOCK = """
  /* ========== 工作台 · 整合自 AI 跟进概要 ========== */
  .time-filter {
    display: flex;
    gap: 0;
    border: 1px solid var(--border-base);
    border-radius: 4px;
    overflow: hidden;
    width: fit-content;
    margin-bottom: 16px;
  }
  .time-filter button {
    background: #fff;
    border: none;
    padding: 6px 14px;
    font-size: 13px;
    color: var(--text-regular);
    cursor: pointer;
    border-right: 1px solid var(--border-base);
  }
  .time-filter button:last-child { border-right: none; }
  .time-filter button:hover { background: var(--bg-base); }
  .time-filter button.active { background: var(--primary); color: #fff; }

  .card {
    background: #fff;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    border: 1px solid var(--border-extra-light);
  }
  .card-header {
    padding: 14px 18px;
    border-bottom: 1px solid var(--border-extra-light);
    display: flex; align-items: center;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-main);
  }
  .card-header .actions {
    margin-left: auto;
    display: flex; gap: 8px; align-items: center;
    font-size: 12px;
    font-weight: normal;
    color: var(--text-secondary);
  }
  .card-body { padding: 18px; }
  .card-body.flush { padding: 0; }

  .kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 16px;
  }
  .kpi-card.kpi-danger {
    background: #fff;
    border-radius: 6px;
    padding: 18px 20px;
    border: 1px solid var(--border-extra-light);
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
    position: relative;
    overflow: hidden;
    color: inherit;
    text-decoration: none;
    display: block;
  }
  .kpi-card.kpi-danger:hover,
  .kpi-card.kpi-primary:hover,
  .kpi-card.kpi-success:hover,
  .kpi-card.kpi-warning:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }
  .kpi-card.kpi-primary,
  .kpi-card.kpi-success,
  .kpi-card.kpi-warning {
    background: #fff;
    border-radius: 6px;
    padding: 18px 20px;
    border: 1px solid var(--border-extra-light);
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
    position: relative;
    overflow: hidden;
    color: inherit;
    text-decoration: none;
    display: block;
  }
  .kpi-card.kpi-danger::after,
  .kpi-card.kpi-primary::after,
  .kpi-card.kpi-success::after,
  .kpi-card.kpi-warning::after {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
  }
  .kpi-card.kpi-danger::after { background: var(--danger); }
  .kpi-card.kpi-primary::after { background: var(--primary); }
  .kpi-card.kpi-success::after { background: var(--success); }
  .kpi-card.kpi-warning::after { background: var(--warning); }
  .kpi-card.kpi-danger { animation: kpi-pulse 2s infinite; }
  @keyframes kpi-pulse {
    0%, 100% { box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 0 0 0 rgba(245,108,108,0); }
    50% { box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 0 0 4px rgba(245,108,108,0.08); }
  }
  .kpi-value {
    margin-top: 8px;
    font-size: 32px;
    font-weight: 700;
    line-height: 1;
    color: var(--text-main);
  }
  .kpi-value.text-danger { color: var(--danger); }
  .kpi-value.text-primary { color: var(--primary); }
  .kpi-value.text-success { color: var(--success); }
  .kpi-value.text-warning { color: var(--warning); }
  .kpi-foot .delta-up { color: var(--success); }
  .kpi-foot .delta-down { color: var(--danger); }
  .kpi-foot {
    margin-top: 8px;
    font-size: 12px;
    color: var(--text-secondary);
    display: flex; align-items: center; gap: 8px;
  }
  .kpi-label {
    font-size: 13px;
    color: var(--text-secondary);
    display: flex; align-items: center; gap: 6px;
  }

  .life-dist { display: flex; flex-direction: column; gap: 10px; }
  .life-row {
    display: grid;
    grid-template-columns: 96px 1fr 36px;
    align-items: center;
    gap: 10px;
    font-size: 13px;
  }
  .life-label { color: var(--text-regular); text-align: right; }
  .life-bar-track {
    height: 10px;
    background: #F5F7FA;
    border-radius: 999px;
    overflow: hidden;
  }
  .life-bar { height: 100%; border-radius: 999px; min-width: 4px; }
  .life-val { font-weight: 700; color: var(--text-main); text-align: right; }
  .stage-chip {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 999px;
    background: #ECF5FF;
    color: #419EFE;
    font-size: 12px;
    font-weight: 500;
  }

  .charts-row {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 16px;
    margin-bottom: 16px;
  }
  .charts-row-2 {
    display: grid;
    grid-template-columns: 1fr 1.4fr;
    gap: 16px;
    margin-bottom: 16px;
  }
  .chart { height: 280px; }
  .chart-tall { height: 320px; }

  table.exception-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  table.exception-table th {
    background: var(--bg-base);
    color: var(--text-regular);
    font-weight: 500;
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border-light);
  }
  table.exception-table td {
    padding: 12px;
    border-bottom: 1px solid var(--border-extra-light);
    color: var(--text-regular);
  }
  table.exception-table tr:last-child td { border-bottom: none; }
  table.exception-table tr:hover td { background: var(--bg-base); }

  .tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 11px;
    line-height: 16px;
    background: var(--bg-base);
    color: var(--text-secondary);
  }
  .tag-danger { background: var(--danger-soft-bg); color: var(--danger); }
  .tag-warning { background: var(--warning-soft-bg); color: var(--warning); }
  .tag-primary { background: var(--primary-soft-bg); color: var(--primary); }
  .tag-success { background: var(--success-soft-bg); color: var(--success); }

  .link-btn { color: var(--primary); cursor: pointer; font-size: 12px; }
  .link-btn:hover { text-decoration: underline; }
"""

# ========== 2. JS 注入 ==========
JS_BLOCK = """
<!-- ECharts CDN + 4 图表 -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<script>
(function () {
  var PRIMARY = '#419EFE';
  var SUCCESS = '#67C23A';
  var WARNING = '#E6A23C';
  var DANGER = '#F56C6C';
  var TEXT_MAIN = '#303133';
  var TEXT_SECONDARY = '#909399';

  function initChart(id, option) {
    var el = document.getElementById(id);
    if (!el) return;
    var chart = echarts.init(el);
    chart.setOption(option);
    window.addEventListener('resize', function () { chart.resize(); });
    return chart;
  }

  // ========== 趋势折线图 ==========
  initChart('chart-trend', {
    grid: { left: 40, right: 16, top: 30, bottom: 30 },
    legend: { top: 0, left: 'left', icon: 'circle', itemWidth: 8, itemHeight: 8, textStyle: { fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['8/26', '8/27', '8/28', '8/29', '8/30', '8/31', '9/1'],
      axisLine: { lineStyle: { color: '#DCDFE6' } },
      axisLabel: { color: TEXT_SECONDARY, fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#F2F6FC' } },
      axisLabel: { color: TEXT_SECONDARY, fontSize: 11 }
    },
    series: [
      {
        name: 'AI 接管',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        data: [12, 15, 18, 14, 16, 20, 22],
        itemStyle: { color: PRIMARY },
        lineStyle: { width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(65, 158, 254, 0.3)' },
            { offset: 1, color: 'rgba(65, 158, 254, 0)' }
          ])
        }
      },
      {
        name: '转人工',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        data: [3, 5, 4, 6, 5, 7, 8],
        itemStyle: { color: DANGER },
        lineStyle: { width: 2 }
      },
      {
        name: '已超时',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        data: [1, 0, 2, 1, 3, 2, 4],
        itemStyle: { color: WARNING },
        lineStyle: { width: 2 }
      }
    ]
  });

  // ========== 转化漏斗图 ==========
  initChart('chart-funnel', {
    tooltip: { trigger: 'item', formatter: '{b}: {c}' },
    series: [{
      type: 'funnel',
      left: '10%',
      right: '10%',
      top: 20,
      bottom: 20,
      width: '80%',
      min: 0,
      max: 100,
      minSize: '0%',
      maxSize: '100%',
      sort: 'descending',
      gap: 2,
      label: {
        show: true,
        position: 'inside',
        formatter: '{b}: {c}',
        color: '#fff',
        fontSize: 12,
        fontWeight: 600
      },
      labelLine: { show: false },
      itemStyle: { borderColor: '#fff', borderWidth: 1 },
      data: [
        { value: 100, name: '线索总数', itemStyle: { color: PRIMARY } },
        { value: 78, name: 'AI 接管', itemStyle: { color: '#5BACFF' } },
        { value: 42, name: '转人工', itemStyle: { color: WARNING } },
        { value: 28, name: '销售跟进', itemStyle: { color: '#67C23A' } },
        { value: 12, name: '成交', itemStyle: { color: SUCCESS } }
      ]
    }]
  });

  // ========== SLA 环图 ==========
  initChart('chart-sla', {
    tooltip: { trigger: 'item' },
    title: {
      text: '73%',
      left: 'center',
      top: '38%',
      textStyle: { color: TEXT_MAIN, fontSize: 28, fontWeight: 700 }
    },
    graphic: [
      { type: 'text', left: 'center', top: '52%', style: { text: '达标率', fill: TEXT_SECONDARY, fontSize: 12 } }
    ],
    legend: {
      bottom: 0,
      left: 'center',
      icon: 'circle',
      itemWidth: 8,
      itemHeight: 8,
      textStyle: { fontSize: 11, color: TEXT_SECONDARY }
    },
    series: [{
      type: 'pie',
      radius: ['62%', '78%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      label: { show: false },
      labelLine: { show: false },
      data: [
        { value: 73, name: '30 分钟内响应', itemStyle: { color: SUCCESS } },
        { value: 18, name: '30-60 分钟', itemStyle: { color: WARNING } },
        { value: 9, name: '超时', itemStyle: { color: DANGER } }
      ]
    }, {
      type: 'pie',
      radius: ['0%', '58%'],
      label: { show: false },
      data: [{ value: 1, itemStyle: { color: 'transparent' } }],
      silent: true
    }]
  });

  // ========== 车型热度 Top 5 ==========
  initChart('chart-cars', {
    grid: { left: 90, right: 50, top: 10, bottom: 30 },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#F2F6FC' } },
      axisLabel: { color: TEXT_SECONDARY, fontSize: 11 }
    },
    yAxis: {
      type: 'category',
      data: ['JAC E10X', 'Tiguan', 'XPENG G6', 'BYD Dolphin', 'Jetta'],
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: TEXT_MAIN, fontSize: 12 }
    },
    series: [{
      type: 'bar',
      barWidth: 14,
      data: [
        { value: 38, itemStyle: { color: PRIMARY } },
        { value: 32, itemStyle: { color: '#5BACFF' } },
        { value: 28, itemStyle: { color: '#7CC4FF' } },
        { value: 19, itemStyle: { color: '#A0D2FF' } },
        { value: 15, itemStyle: { color: '#C5E0FF' } }
      ],
      label: { show: true, position: 'right', color: TEXT_MAIN, fontSize: 11 }
    }]
  });
})();
</script>
"""

# 幂等检查
if 'initChart(\'chart-trend\'' in html:
    print("⚠️  ECharts JS 已存在，跳过注入")
else:
    # CSS 注入到 </style> 前
    if '/* ========== 工作台 · 整合自 AI 跟进概要 ========== */' not in html:
        html = html.replace('</style>', CSS_BLOCK + '\n</style>', 1)
        print("✅ CSS 已注入")
    else:
        print("⚠️  CSS 已存在，跳过")

    # JS 注入到 </body> 前
    if '<!-- ECharts CDN + 4 图表 -->' not in html:
        html = html.replace('</body>', JS_BLOCK + '\n</body>', 1)
        print("✅ JS 已注入")
    else:
        print("⚠️  JS 已存在，跳过")

TARGET.write_text(html, encoding='utf-8')
print(f"✅ 文件已更新：{TARGET}")
print(f"   文件总长：{len(html)}")