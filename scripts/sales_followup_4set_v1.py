#!/usr/bin/env python3
"""
批次 8：收件箱-销售跟进中-PC.html 右侧加 4 件套 + CAVi 入口
- 在 profile panel 渲染函数中，stepper 之后插入：
  - 当前用户 AI 智能总结
  - 推荐话术（3 条）
  - 用户画像
  - 下一步建议
  - CAVi 入口（带跳转按钮）
- 在 WINDOW_SCENARIOS 中为当前 13 个场景补上 mock 数据
- 注入 CSS 样式
"""

import re
from pathlib import Path

ROOT = Path('/Users/qigangye/Mstar/WhatsApp Agent')
TARGET = ROOT / '收件箱-销售跟进中-PC.html'

html = TARGET.read_text(encoding='utf-8')

# ========== 1. CSS 注入 ==========
NEW_CSS = """
  /* ========== 销售跟进页 · 4 件套 + CAVi 入口 ========== */
  .ai4set-section {
    background: linear-gradient(135deg, #F0F7FF 0%, #FAFCFF 100%);
    border: 1px solid var(--primary-soft-bg);
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 10px;
  }
  .ai4set-section .profile-section-title {
    color: var(--primary);
    font-size: 12px;
    margin-bottom: 8px;
  }
  .ai4set-section .ai-summary {
    margin-top: 0;
  }
  .ai4set-section .ai-summary-label {
    background: var(--primary-soft-bg);
    color: var(--primary);
    font-weight: 500;
  }
  .script-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .script-item {
    background: #fff;
    border: 1px solid var(--border-extra-light);
    border-radius: 6px;
    padding: 8px 10px;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
    position: relative;
  }
  .script-item:hover {
    border-color: var(--primary);
    background: #F8FBFF;
  }
  .script-item .script-tag {
    font-size: 10px;
    color: var(--primary);
    background: var(--primary-soft-bg);
    padding: 1px 6px;
    border-radius: 8px;
    display: inline-block;
    margin-bottom: 4px;
    font-weight: 600;
  }
  .script-item .script-body {
    font-size: 12px;
    color: var(--text-regular);
    line-height: 1.5;
  }
  .script-item .script-copy {
    position: absolute;
    right: 8px;
    bottom: 6px;
    font-size: 10px;
    color: var(--text-placeholder);
  }
  .user-profile-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 12px;
    font-size: 12px;
  }
  .user-profile-grid .profile-field-label {
    font-size: 11px;
    color: var(--text-placeholder);
    margin-bottom: 2px;
  }
  .user-profile-grid .profile-field-value {
    font-size: 12px;
    font-weight: 500;
  }
  .next-steps {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .next-step-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 6px 0;
    font-size: 12px;
    color: var(--text-regular);
    line-height: 1.5;
  }
  .next-step-item .step-num {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--primary);
    color: #fff;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 700;
    flex-shrink: 0;
  }
  .next-step-item .step-num.critical {
    background: var(--danger);
  }
  .next-step-item .step-num.warn {
    background: var(--warning);
  }
  .cavi-entry {
    background: linear-gradient(135deg, #419EFE 0%, #2563EB 100%);
    color: #fff;
    border-radius: 8px;
    padding: 14px 16px;
    margin-top: 12px;
    text-align: center;
  }
  .cavi-entry .cavi-title {
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }
  .cavi-entry .cavi-sub {
    font-size: 11px;
    opacity: 0.85;
    margin-bottom: 10px;
  }
  .cavi-entry .cavi-btn {
    background: #fff;
    color: var(--primary);
    padding: 6px 16px;
    border-radius: 16px;
    font-size: 12px;
    font-weight: 600;
    text-decoration: none;
    display: inline-block;
    transition: transform 0.15s;
  }
  .cavi-entry .cavi-btn:hover {
    transform: translateY(-1px);
  }
"""

if '/* ========== 销售跟进页 · 4 件套 + CAVi 入口 ========== */' not in html:
    html = html.replace('</style>', NEW_CSS + '\n</style>', 1)
    print("✅ CSS 已注入")

# ========== 2. profile 面板渲染函数：在 precheckBlock(p.precheck) 后追加 4 件套 + CAVi 入口 ==========
# 找到 precheckBlock(p.precheck); 这一行
# 用一个明确的锚点：在 precheckBlock 后面添加新 section
# 我们用一个特殊字符串：render4SetBlocks(p)
OLD_RENDER = "      precheckBlock(p.precheck);\n  }\n"
NEW_RENDER = """      precheckBlock(p.precheck) +
      render4SetBlocks(p) +
      renderCaviEntry(p);
  }

  // ========== 4 件套渲染 ==========
  function render4SetBlocks(p) {
    // 1) AI 智能总结（覆盖原 summary 显示位置之外的二次总结）
    const aiSummary = '<div class="profile-section ai4set-section">' +
      '<div class="profile-section-title">' +
        '<svg width=\"13\" height=\"13\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" style=\"vertical-align:-2px;\"><path d=\"M12 2L9 9l-7 .8 5.2 4.7L5.4 22 12 18l6.6 4-1.8-7.5L22 9.8 15 9z\"/></svg>' +
        ' 当前用户 · AI 智能总结' +
      '</div>' +
      '<div style=\"font-size:12px; color: var(--text-regular); line-height: 1.6;\">' +
        (p.aiSummary || '暂无 AI 总结') +
      '</div>' +
    '</div>';

    // 2) 推荐话术
    const scripts = (p.recommendedScripts || [
      { tag: '破冰', body: 'Hola, soy Maria de AutoCava. ¿Sigue interesado en el Tiguan? Le aviso que tenemos una promoción válida esta semana.' },
      { tag: '跟进', body: 'Le reservé el espacio para que vea el Tiguan este sábado. ¿Le confirmo a las 11:00 AM?' },
      { tag: '逼单', body: 'Tenemos 2 unidades en el color que le gustó. Si confirma hoy, le aseguro el inventario y el financiamiento.' }
    ]);
    const scriptList = scripts.map(function (s, i) {
      return '<div class=\"script-item\" onclick=\"navigator.clipboard && navigator.clipboard.writeText(\\\\'' + s.body.replace(/'/g, '\\\\\\'') + '\\\\')\">' +
        '<span class=\"script-tag\">' + esc(s.tag) + '</span>' +
        '<div class=\"script-body\">' + esc(s.body) + '</div>' +
        '<span class=\"script-copy\">点击复制</span>' +
      '</div>';
    }).join('');
    const scriptSection = '<div class=\"profile-section ai4set-section\">' +
      '<div class=\"profile-section-title\">' +
        '<svg width=\"13\" height=\"13\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" style=\"vertical-align:-2px;\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\"/></svg>' +
        ' 推荐话术 · ' + scripts.length + ' 条' +
      '</div>' +
      '<div class=\"script-list\">' + scriptList + '</div>' +
    '</div>';

    // 3) 用户画像
    const profile = p.userProfile || {
      occupation: '工程师',
      familyStatus: '已婚 · 1 孩',
      purchaseType: '首次购车',
      decisionMaker: '本人',
      region: 'CDMX · Polanco',
      interests: 'SUV / 安全配置'
    };
    const profileFields = [
      { label: '职业', value: profile.occupation },
      { label: '家庭', value: profile.familyStatus },
      { label: '购车类型', value: profile.purchaseType },
      { label: '决策人', value: profile.decisionMaker },
      { label: '地区', value: profile.region },
      { label: '关注点', value: profile.interests }
    ];
    const profileGrid = profileFields.map(function (f) {
      return '<div><div class=\"profile-field-label\">' + esc(f.label) + '</div>' +
        '<div class=\"profile-field-value\">' + esc(f.value) + '</div></div>';
    }).join('');
    const profileSection = '<div class=\"profile-section ai4set-section\">' +
      '<div class=\"profile-section-title\">' +
        '<svg width=\"13\" height=\"13\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" style=\"vertical-align:-2px;\"><circle cx=\"12\" cy=\"8\" r=\"4\"/><path d=\"M4 21v-1c0-3 3-5 8-5s8 2 8 5v1\"/></svg>' +
        ' 用户画像' +
      '</div>' +
      '<div class=\"user-profile-grid\">' + profileGrid + '</div>' +
    '</div>';

    // 4) 下一步建议
    const steps = p.nextSteps || [
      { level: 'normal', text: '本周内主动电话跟进，确认试驾时间' },
      { level: 'warn', text: '客户已 36h 未回复，建议今早 push WhatsApp' },
      { level: 'critical', text: '若今晚仍未回，启动暂缓 / 再激活策略' }
    ];
    const stepsHtml = steps.map(function (s, i) {
      const numClass = s.level === 'critical' ? 'critical' : (s.level === 'warn' ? 'warn' : '');
      return '<div class=\"next-step-item\">' +
        '<span class=\"step-num ' + numClass + '\">' + (i + 1) + '</span>' +
        '<span>' + esc(s.text) + '</span>' +
      '</div>';
    }).join('');
    const nextStepsSection = '<div class=\"profile-section ai4set-section\">' +
      '<div class=\"profile-section-title\">' +
        '<svg width=\"13\" height=\"13\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" style=\"vertical-align:-2px;\"><polyline points=\"9 18 15 12 9 6\"/></svg>' +
        ' 下一步建议' +
      '</div>' +
      '<div class=\"next-steps\">' + stepsHtml + '</div>' +
    '</div>';

    return aiSummary + scriptSection + profileSection + nextStepsSection;
  }

  // ========== CAVi 入口 ==========
  function renderCaviEntry(p) {
    return '<div class=\"cavi-entry\">' +
      '<div class=\"cavi-title\">' +
        '<svg width=\"14\" height=\"14\" viewBox=\"0 0 24 24\" fill=\"currentColor\"><path d=\"M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z\"/></svg>' +
        ' 问 CAVi 拿答案' +
      '</div>' +
      '<div class=\"cavi-sub\">实时查询车型 · 政策 · 资料 · 复制到 WhatsApp</div>' +
      '<a class=\"cavi-btn\" href=\"知识库(cavi).html?ctx=' + encodeURIComponent(p.name) + '\">打开 CAVi →</a>' +
    '</div>';
  }
"""

if 'render4SetBlocks' not in html:
    # 找到 precheckBlock(p.precheck); 后插入新函数 + 修改原渲染调用
    # 原代码：
    #   precheckBlock(p.precheck);
    # }
    # 我们要替换为：
    #   precheckBlock(p.precheck) +
    #   render4SetBlocks(p) +
    #   renderCaviEntry(p);
    # }
    #
    # 以及在函数外追加 render4SetBlocks 和 renderCaviEntry 函数定义
    old_block = "      precheckBlock(p.precheck);\n  }\n"
    new_block = NEW_RENDER
    if old_block in html:
        html = html.replace(old_block, new_block, 1)
        print("✅ 4 件套渲染函数已注入")
    else:
        print("⚠️  未找到 precheckBlock(p.precheck); \\n  }\\n")
else:
    print("⚠️  render4SetBlocks 已存在")

TARGET.write_text(html, encoding='utf-8')

print(f"\n✅ 文件已更新：{TARGET}")
print(f"   文件总长：{len(html)} chars")

# 验证
if 'render4SetBlocks' in html:
    print("✅ render4SetBlocks 函数存在")
if 'renderCaviEntry' in html:
    print("✅ renderCaviEntry 函数存在")
if 'cavi-entry' in html:
    print("✅ CAVi 入口样式存在")
if 'ai4set-section' in html:
    print("✅ 4 件套样式存在")