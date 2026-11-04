import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="슈퍼마켓 판매 대시보드", layout="wide")
st.title("🏪 슈퍼마켓 판매 데이터 대시보드")

# 1. 데이터 불러오기
@st.cache_data
def load_data():
    # app.py와 같은 폴더의 Sales.xlsx 파일 읽기 (시트명: supermarket_sales_test)
    df = pd.read_excel("Sales.xlsx", sheet_name="supermarket_sales_test")
    # 결측치 제거
    df = df.dropna()
    return df

try:
    df = load_data()

    # 2. 사이드바 - 지점(Branch) 선택
    branches = sorted(df["Branch"].unique())
    selected_branch = st.sidebar.selectbox("지점(Branch) 선택", branches)

    # 선택한 지점 데이터 필터링
    filtered_df = df[df["Branch"] == selected_branch]

    # 3. 메트릭 계산 (총매출, 평균매출, 평균 평점)
    # 매출 컬럼명은 데이터셋에 맞춰 'Total' 또는 'gross income' 등이 될 수 있으므로,
    # 일반적인 supermarket sales 데이터 구조의 'Total'과 'Rating' 컬럼을 기준으로 작성했습니다.
    total_sales = filtered_df["Total"].sum()
    avg_sales = filtered_df["Total"].mean()
    avg_rating = filtered_df["Rating"].mean()

    # 메트릭 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f"{selected_branch} 지점 총 매출", value=f"${total_sales:,.2f}")
    with col2:
        st.metric(label="평균 매출", value=f"${avg_sales:,.2f}")
    with col3:
        st.metric(label="평균 평점 (Rating)", value=f"⭐ {avg_rating:.2f} / 10")

    st.markdown("---")

    # 4. 상품 카테고리(Product line)별 평균 매출 시각화
    # 그룹화 및 평균 계산
    category_sales = (
        filtered_df.groupby("Product line")["Total"]
        .mean()
        .reset_index()
        .sort_values(by="Total", ascending=False)
    )

    st.subheader("🛍️ 상품 카테고리별 평균 매출")
    fig = px.bar(
        category_sales,
        x="Product line",
        y="Total",
        text_auto=".2f",
        labels={"Total": "평균 매출 ($)", "Product line": "상품 카테고리"},
        color="Total",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("Sales.xlsx 파일을 찾을 수 없습니다. app.py와 동일한 경로에 파일을 업로드해주세요.")
except Exception as e:
    st.error(f"에러가 발생했습니다: {e}")
