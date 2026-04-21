
import streamlit as st
import numpy as np

st.set_page_config(page_title="认知风险评估", page_icon="🧠")

st.title("癫痫患儿认知风险评估")
st.write("验证组 AUC = 0.739 | 基于巢式病例对照研究")

# 模型系数
INTERCEPT = -2.5903
COEF_TOXICITY = 1.100
COEF_COUNT = 0.786
COEF_SEIZURE = 0.802

# 药物风险分组
high_risk = ["托吡酯（妥泰）", "苯巴比妥", "氯硝西泮"]
mid_risk = ["丙戊酸钠（德巴金）"]
low_risk = ["左乙拉西坦", "拉莫三嗪", "奥卡西平", "拉考沙胺", "吡仑帕奈"]
all_drugs = low_risk + mid_risk + high_risk

st.subheader("临床信息")

# 药物选择
drugs = st.multiselect("抗癫痫药物（可多选）", all_drugs)

# 计算风险等级
risk = 1
if drugs:
    for d in drugs:
        if d in high_risk:
            risk = 3
            break
        elif d in mid_risk:
            risk = 2
    st.write(f"**用药风险等级：{risk} 级**")
else:
    st.info("请选择药物")

# 用药数量
drug_num = st.selectbox("用药数量", [1, 2, 3])

# 发作类型
seizure_type = st.radio("发作类型", ["局灶性/BECTS/失神", "全面性发作"])

st.divider()

# 评估按钮
if st.button("评估认知损伤风险", type="primary"):
    if drugs:
        seizure = 1 if seizure_type == "全面性发作" else 0
        score = INTERCEPT + COEF_TOXICITY * risk + COEF_COUNT * drug_num + COEF_SEIZURE * seizure
        prob = 1 / (1 + np.exp(-score))
        
        st.subheader("评估结果")
        
        col1, col2 = st.columns(2)
        col1.metric("风险概率", f"{prob*100:.1f}%")
        
        if prob < 0.5:
            col2.success("低风险")
            advice = "常规随访"
        elif prob < 0.7:
            col2.warning("中风险")
            advice = "加强认知监测"
        else:
            col2.error("高风险")
            advice = "早期康复干预，优化用药"
        
        st.info(f"💡 建议：{advice}")
        
        with st.expander("查看详细计算"):
            st.write(f"药物：{', '.join(drugs)}")
            st.write(f"风险等级：{risk}")
            st.write(f"用药数量：{drug_num}")
            st.write(f"发作类型：{seizure_type}")
            st.write(f"风险评分：{score:.4f}")
    else:
        st.error("请至少选择一种药物")

st.caption("⚠️ 仅供参考，不能替代临床医生判断")