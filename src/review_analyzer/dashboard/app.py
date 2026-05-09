from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

from review_analyzer.core.config import get_settings

_SETTINGS = get_settings()
API_URL = _SETTINGS.api_url.rstrip("/")
SENTIMENT_SCORE = {"negative": -1, "neutral": 0, "positive": 1}


def analyze_review(review_text: str, product_id: str | None) -> dict[str, object]:
    response = requests.post(
        f"{API_URL}/analyze",
        json={"review_text": review_text, "product_id": product_id or None},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def render_tags(tags: list[str]) -> None:
    tag_html = " ".join(f"<span class='tag'>{tag}</span>" for tag in tags)
    st.markdown(tag_html, unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="Review Analyzer", page_icon="RA", layout="wide")
    st.markdown(
        """
        <style>
        .main .block-container { padding-top: 2rem; max-width: 1180px; }
        .tag {
            display: inline-block;
            padding: 0.25rem 0.55rem;
            margin: 0.15rem 0.2rem 0.15rem 0;
            border-radius: 6px;
            background: #eef2ff;
            color: #1e3a8a;
            font-size: 0.85rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Intelligent Product Review Analyzer")

    left, right = st.columns([0.58, 0.42], gap="large")
    with left:
        product_id = st.text_input("Product ID", value="B001234")
        review_text = st.text_area(
            "Review",
            value="The product quality is great but delivery was very slow. Packaging was damaged.",
            height=190,
        )
        submitted = st.button("Analyze Review", type="primary")

    with right:
        st.metric("API", API_URL)
        st.caption("Set API_URL to point the dashboard at a different backend.")

    if not submitted:
        return

    if not review_text.strip():
        st.error("Enter a review to analyze.")
        return

    try:
        result = analyze_review(review_text, product_id)
    except requests.RequestException as exc:
        st.error(f"Unable to analyze review: {exc}")
        return

    st.divider()
    summary_cols = st.columns(2)
    summary_cols[0].metric("Overall sentiment", str(result["overall_sentiment"]).title())
    summary_cols[1].metric("Aspects found", len(result["aspects"]))

    chart_col, detail_col = st.columns([0.55, 0.45], gap="large")

    with chart_col:
        aspects = result["aspects"]
        if aspects:
            chart_data = pd.DataFrame(
                [
                    {"aspect": aspect, "score": SENTIMENT_SCORE.get(sentiment, 0)}
                    for aspect, sentiment in aspects.items()
                ]
            ).set_index("aspect")
            st.subheader("Aspect Sentiment")
            st.bar_chart(chart_data, y="score")
            st.dataframe(
                pd.DataFrame(
                    [
                        {"aspect": aspect, "sentiment": sentiment}
                        for aspect, sentiment in aspects.items()
                    ]
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No configured aspects were detected in this review.")

    with detail_col:
        st.subheader("Tags")
        render_tags(list(result["tags"]))

        st.subheader("Aspect Terms")
        st.json(result["aspect_terms"])

    with st.expander("Pipeline Details"):
        st.write("Cleaned text")
        st.code(str(result["cleaned_text"]))
        st.write("Normalized tokens")
        st.write(result["normalized_tokens"])


if __name__ == "__main__":
    main()
