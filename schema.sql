CREATE TABLE IF NOT EXISTS watch_items (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  status ENUM('to_watch','watching','finished') NOT NULL DEFAULT 'to_watch',
  note TEXT NULL,
  year VARCHAR(10) NULL,
  runtime VARCHAR(20) NULL,
  poster_url TEXT NULL,
  plot TEXT NULL,
  imdb_rating DECIMAL(3,1) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
