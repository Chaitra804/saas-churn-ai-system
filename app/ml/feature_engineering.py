def create_features(df):

    if "MonthlyRevenue" in df.columns and "LoginFrequency" in df.columns:

        df["RevenuePerLogin"] = (
            df["MonthlyRevenue"] /
            (df["LoginFrequency"] + 1)
        )

    if "SupportTickets" in df.columns and "SubscriptionLength" in df.columns:

        df["TicketRatio"] = (
            df["SupportTickets"] /
            (df["SubscriptionLength"] + 1)
        )

    return df