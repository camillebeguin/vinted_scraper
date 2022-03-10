#### Preprocessing parameters

# Pages
relevant_cols_pages = [
    "id",
    "title",
    "price",
    "discount",
    "brand_title",
    "is_for_swap",
    "url",
    "promoted",
    "favourite_count",
    "view_count",
    "size_title",
    "user_id",
    "user_login",
    "photo_url",
    "photo_timestamp",
]

colnames_pages = {
    "id": "ad_id",
    "title": "ad_title",
    "brand_title": "brand",
    "url": "ad_url",
    "size_title": "size",
}

coltypes_pages = {"ad_id": "str", "user_id": "str"}

# Ads
time_cols_ads = ["user_created_at", "user_last_loged_on_ts", "details_Ajouté"]

relevant_cols_ads = [
    "ad_id",
    "ad_title",
    "ad_description",
    "user_id",
    "user_login",
    "user_item_count",
    "user_given_item_count",
    "user_taken_item_count",
    "user_forum_msg_count",
    "user_forum_topic_count",
    "user_followers_count",
    "user_following_count",
    "user_following_brands_count",
    "user_positive_feedback_count",
    "user_neutral_feedback_count",
    "user_negative_feedback_count",
    "user_meeting_transaction_count",
    "user_feedback_reputation",
    "user_created_at",
    "user_last_loged_on_ts",
    "user_city",
    "user_country_id",
    "user_country_code",
    "user_country_title",
    "user_bundle_discount",
    "user_business",
    "user_total_items_count",
    "user_about",
    "user_profile_url",
    "user_has_promoted_closet",
    "details_Marque",
    "details_Taille",
    "details_État",
    "details_Couleur",
    "details_Modes de paiement",
    "details_Nombre de vues",
    "details_Intéressés·ées",
    "details_Ajouté",
]

colnames_ads = {
    "details_Marque": "brand",
    "details_Taille": "size",
    "details_État": "condition",
    "details_Couleur": "color",
    "details_Modes de paiement": "payment_methods",
    "details_Nombre de vues": "view_count",
    "details_Intéressés·ées": "favourite_count",
    "details_Ajouté": "ad_posting_date",
}

coltypes_ads = {
    "ad_id": "str",
    "user_id": "str",
    "user_item_count": "float",
    "user_given_item_count": "float",
    "user_taken_item_count": "float",
    "user_forum_msg_count": "float",
    "user_forum_topic_count": "float",
    "user_followers_count": "float",
    "user_following_count": "float",
    "user_following_brands_count": "float",
    "user_positive_feedback_count": "float",
    "user_neutral_feedback_count": "float",
    "user_negative_feedback_count": "float",
    "user_meeting_transaction_count": "float",
    "user_feedback_reputation": "float",
    "user_country_id": "str",
    "user_total_items_count": "float",
    "view_count": "float",
    "favourite_count": "float",
    #"user_created_at": "datetime64[ns]"
}
