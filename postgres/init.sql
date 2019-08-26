create table if not exists conversations (
    cid serial not null
    constraint conversations_pkey
    primary key,
    id integer not null unique,
    name text,
    last_ts integer not null
);

create table if not exists notifications (
    rid serial not null
    constraint reminders_pkey
    primary key,
    type text not null,
    whom integer not null references conversations on delete no action,
    ts integer not null
);