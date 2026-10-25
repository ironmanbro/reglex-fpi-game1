-- Custody Desk League: league table setup.
-- Run once in Supabase: SQL Editor -> New query -> paste -> Run.

create table if not exists public.scores (
  id         bigint generated always as identity primary key,
  name       text        not null check (char_length(btrim(name)) between 1 and 24),
  score      integer     not null check (score between 0 and 7500),
  correct    integer     not null check (correct >= 0),
  total      integer     not null check (total in (10, 15, 20, 25)),
  created_at timestamptz not null default now(),
  check (correct <= total),
  check (score <= correct * 300)
);

create index if not exists scores_score_idx on public.scores (score desc, created_at);

-- Visitors can read the table and add a score. Nobody can edit or delete
-- through the website; you can remove rows yourself in the Table Editor.
alter table public.scores enable row level security;

drop policy if exists "Anyone can read scores" on public.scores;
create policy "Anyone can read scores" on public.scores
  for select to anon, authenticated using (true);

drop policy if exists "Anyone can add a score" on public.scores;
create policy "Anyone can add a score" on public.scores
  for insert to anon, authenticated with check (true);

grant select, insert on public.scores to anon, authenticated;

-- Supabase grants extra rights by default; keep visitors to read + add only.
revoke update, delete, truncate, references, trigger on public.scores from anon, authenticated;
