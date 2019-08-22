create table if not exists conversations (
    cid serial not null
    constraint conversations_pkey
    primary key,
    id integer not null unique,
    name text
);