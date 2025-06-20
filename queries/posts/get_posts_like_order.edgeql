with post := (select Paper::Post {
  paper_id
} filter .modified >= <datetime>$start_date and .modified <= <datetime>$end_date)
select post {paper_id} order by .like_count desc limit 10;

