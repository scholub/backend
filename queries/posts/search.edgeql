select Paper::Post {
  paper_id,
  cosine_similarity := 1 - ext::pgvector::cosine_distance(
    .embedding, <Paper::Embedding>$embedding
  )
} order by ext::pgvector::cosine_distance(
  .embedding, <Paper::Embedding>$embedding
) limit <int64>$limit;
