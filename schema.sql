CREATE TABLE public.movies (
    id SERIAL PRIMARY KEY,
    name text NOT NULL,
    year integer NOT NULL
);

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(500) NOT NULL,
    admin boolean NOT NULL,
    CONSTRAINT unique_username UNIQUE (username)
    CONSTRAINT min_username_length CHECK (LENGTH(username) >= 3);
);

CREATE TABLE public.reviews (
    id SERIAL PRIMARY KEY,
    content text,
    score integer,
    user_id integer REFERENCES users,
    movie_id integer REFERENCES movies,
    sent_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT reviews_score_check CHECK (score >= 0 AND score <= 10)
);

CREATE TABLE public.likes (
    id SERIAL PRIMARY KEY,
    liketype VARCHAR(10),
    user_id integer REFERENCES users,
    review_id integer REFERENCES reviews,
    CONSTRAINT unique_like_dislike UNIQUE (user_id, review_id)
);
