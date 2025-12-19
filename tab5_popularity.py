import streamlit as st
import pandas as pd
import plotly.express as px


def _add_popularity_measure(df: pd.DataFrame) -> pd.DataFrame:
    #use spotify popularity when available; otherwise fall back to an appearances proxy
    df_out = df.copy()

    if "popularity" in df_out.columns:
        df_out["popularity_measure"] = pd.to_numeric(df_out["popularity"], errors="coerce")
        df_out["popularity_label"] = "Spotify Popularity (Dataset Field)"
        return df_out

    #count how often a song appears in the dataset
    song_counts = (
        df_out.groupby(["artist", "song"])
        .size()
        .reset_index(name="appearances")
    )

    df_out = df_out.merge(song_counts, on=["artist", "song"], how="left")
    df_out["popularity_measure"] = df_out["appearances"].astype(float)
    df_out["popularity_label"] = "Popularity Proxy (Appearances in Dataset)"
    return df_out


def _build_response_curve(df: pd.DataFrame, feature: str, bins: int = 20) -> pd.DataFrame:
    #bin feature values to reduce noise and show the overall direction of association
    working = df[[feature, "popularity_measure"]].dropna().copy()

    if working.empty:
        return pd.DataFrame(columns=["feature_mean", "popularity_mean"])

    #qcut creates quantile bins, which keeps bin sizes more balanced
    working["feature_bin"] = pd.qcut(working[feature], q=bins, duplicates="drop")

    response_df = (
        working.groupby("feature_bin", observed=True)
        .agg(
            feature_mean=(feature, "mean"),
            popularity_mean=("popularity_measure", "mean"),
            n=("popularity_measure", "size"),
        )
        .reset_index(drop=True)
        .sort_values("feature_mean")
    )

    return response_df


def show_popularity_mechanisms(df: pd.DataFrame):
    """
    tab 5: popularity mechanisms

    goal: show whether certain encoded features are associated with higher platform visibility
    method: response curves (feature level increases on x, average popularity on y)
    """

    st.header("Popularity Mechanisms: What Gets Rewarded?")

    st.markdown(
        """
        The question here is not whether genres should converge, but why they might.

        If genres drift toward particular sonic features over time, one possibility is that those
        features are associated with higher platform visibility. This section asks one focused question:

        **How does popularity change as specific audio features increase?**

        Instead of comparing discrete groups of songs, this page shows response curves that visualize
        gradual shifts. This helps connect feature trends to platform-facing “reward,” without treating
        association as causation.
        """
    )

    st.markdown("---")

    #prepare the popularity measure used for the y-axis
    df_pop = _add_popularity_measure(df)

    popularity_label = df_pop["popularity_label"].iloc[0] if len(df_pop) > 0 else "Popularity"
    
    st.subheader("Feature Selection for This Section")

    st.markdown(
        """
        This section focuses on **danceability** and **energy** because they are especially understandable as
        platform-relevant features. They map cleanly onto playlist contexts such as workout, party,
        and background listening, where repeated circulation can translate into sustained visibility.

        Other features such as **valence** help describe emotional range, but they are less directly aligned
        with platform incentive structures. The goal here is not to test every feature, but to examine
        features that plausibly operate as rewarded dimensions in a platform environment.
        """
    )

    st.markdown("---")
    st.subheader("Feature to Popularity Response Curves")

    st.markdown(
        f"""
        Each curve shows how average popularity changes as a feature increases.

        **Y-axis:** {popularity_label}  
        **X-axis:** Average feature value within each bin

        This does not model prediction and does not establish causation. It is a descriptive way to show
        whether the platform-visible songs in this dataset tend to cluster around certain feature ranges.
        """
    )

    st.markdown("---")

    features = ["danceability", "energy"]

    for feature in features:
        if feature not in df_pop.columns:
            st.warning(f"Skipping {feature} because it is not in the dataset.")
            continue

        response_df = _build_response_curve(df_pop, feature=feature, bins=20)

        if response_df.empty:
            st.warning(f"Not enough data to plot a response curve for {feature}.")
            continue

        fig = px.line(
            response_df,
            x="feature_mean",
            y="popularity_mean",
            markers=True,
            title=f"Popularity Response to {feature.capitalize()}",
            labels={
                "feature_mean": feature.capitalize(),
                "popularity_mean": popularity_label,
            },
            template="plotly_dark",
            height=420,
        )

        fig.update_traces(line_width=2)

        st.plotly_chart(fig, use_container_width=True, key=f"{feature}_response_curve")

        st.caption(
            "Points are binned averages (quantiles). This reduces noise and highlights overall direction."
        )

        st.markdown("---")

    st.subheader("How to Read These Curves")
    

    st.markdown(
        """
        An upward slope indicates that higher values of a feature are associated with higher average popularity
        in this dataset. A flat slope indicates little relationship. A downward slope indicates the opposite.

        The effect does not need to be large to matter. If a feature shows a consistent directional association,
        that can create an incentive gradient where small advantages accumulate across many releases over time.
        """
    )

    st.markdown("---")

    st.subheader("Interpretation")

    st.markdown(
        """
        In this dataset, danceability and energy show directional associations with popularity that are consistent
        with the idea of platform-facing reward.

        Seaver’s framing is useful here because it highlights how platforms operationalize “taste” through measurable
        features and systems of recommendation, even when those features are simplifications of musical experience.
        Petrusich’s argument helps explain why genre labels can remain culturally meaningful even when sonic separation
        weakens along the particular dimensions platforms make most visible.

        These curves show alignment between platform-legible audio features and platform-visible outcomes. They do not
        show that any feature causes success, and they do not show that recommendation systems directly dictate artistic choices.
        """
    )

    st.markdown("---")

    st.subheader("Connecting Back to Genre Patterns")

    st.markdown(
        """
        Earlier sections documented feature trends within genres over time. This section adds a mechanism-level lens by showing
        whether the same features are associated with higher visibility in the platform environment.

        If the reward gradient points in a consistent direction, then drift toward that region of feature space becomes easier to explain
        as an outcome of repeated, small adjustments across many artists and releases. This is not a claim of coercion or censorship.
        It is a descriptive claim about how visibility incentives can shape what becomes common at scale.
        """
    )
