-- ============================================================
-- Query 1: Top 10 sources by number of articles published
-- Shows which sources are most active in our dataset
-- ============================================================
SELECT
    source_name,
    COUNT(*) AS article_count,
    ROUND(AVG(reading_time_seconds), 0) AS avg_reading_time_seconds
FROM `affable-framing-464607-b9.news_pipeline.articles`
WHERE source_name IS NOT NULL AND source_name != ''
GROUP BY source_name
ORDER BY article_count DESC
LIMIT 10;


-- ============================================================
-- Query 2: Breaking news vs normal articles summary
-- Shows how many articles were flagged as breaking news
-- ============================================================
SELECT
    is_breaking_news,
    COUNT(*) AS article_count,
    ROUND(AVG(reading_time_seconds), 0) AS avg_reading_time_seconds,
    COUNTIF(has_image = TRUE) AS articles_with_image
FROM `affable-framing-464607-b9.news_pipeline.articles`
GROUP BY is_breaking_news;


-- ============================================================
-- Query 3: Articles by category with average reading time
-- Useful for understanding content depth per category
-- ============================================================
SELECT
    category,
    COUNT(*) AS article_count,
    ROUND(AVG(reading_time_seconds), 0) AS avg_reading_time_seconds,
    COUNTIF(is_breaking_news = TRUE) AS breaking_news_count
FROM `affable-framing-464607-b9.news_pipeline.articles`
WHERE category IS NOT NULL AND category != ''
GROUP BY category
ORDER BY article_count DESC;


-- ============================================================
-- Query 4: Daily ingestion trend
-- Shows how many articles were ingested per day
-- ============================================================
SELECT
    DATE(ingested_at) AS ingestion_date,
    COUNT(*) AS articles_ingested
FROM `affable-framing-464607-b9.news_pipeline.articles`
GROUP BY ingestion_date
ORDER BY ingestion_date DESC;
