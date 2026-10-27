-- Reglex: private score saving, run once.
-- Supabase -> SQL Editor -> New query -> paste all of this -> Run.
-- One row per round, updated after every answer. If a player leaves, the last save is their final score.
-- Visitors can only write through save_round(); nobody but the project owner can read anything.
create table if not exists public.rounds (
  id          uuid primary key,
  name        text        not null check (char_length(name) between 1 and 24),
  total       integer     not null check (total in (10, 15, 20, 25)),
  answered    integer     not null default 0,
  correct     integer     not null default 0,
  score       integer     not null default 0,
  finished    boolean     not null default false,
  answers     jsonb       not null default '[]'::jsonb,
  started_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  check (answered between 0 and total),
  check (correct between 0 and answered),
  check (score between correct * 100 and correct * 300),
  check (jsonb_typeof(answers) = 'array' and jsonb_array_length(answers) <= 25)
);
create index if not exists rounds_updated_idx on public.rounds (updated_at desc);

alter table public.rounds enable row level security;
revoke all on public.rounds from anon, authenticated;

create or replace function public.save_round(
  p_id uuid, p_name text, p_total int, p_answered int, p_correct int,
  p_score int, p_finished boolean, p_answers jsonb
) returns void
language plpgsql security definer set search_path = public as $$
begin
  insert into public.rounds as r (id, name, total, answered, correct, score, finished, answers)
  values (p_id, left(btrim(p_name), 24), p_total, p_answered, p_correct, p_score, coalesce(p_finished, false), coalesce(p_answers, '[]'::jsonb))
  on conflict (id) do update
    set answered = excluded.answered, correct = excluded.correct, score = excluded.score,
        finished = r.finished or excluded.finished, answers = excluded.answers, updated_at = now()
    where excluded.answered >= r.answered and r.name = excluded.name and r.total = excluded.total;
end $$;

revoke all on function public.save_round(uuid, text, int, int, int, int, boolean, jsonb) from public;
grant execute on function public.save_round(uuid, text, int, int, int, int, boolean, jsonb) to anon, authenticated;

-- The old public league table becomes private: visitors may still add (older cached pages), never read.
drop policy if exists "Anyone can read scores" on public.scores;
revoke select on public.scores from anon, authenticated;

-- Owner-only report: newest rounds first. Accuracy counts only the questions actually answered.
create or replace view public.rounds_report with (security_invoker = true) as
  select name, score, correct, answered, total,
         case when finished then 'Completed' else 'Left after ' || answered || ' of ' || total end as status,
         round(100.0 * correct / nullif(answered, 0)) as accuracy_pct,
         started_at, updated_at, id
  from public.rounds order by updated_at desc;
revoke all on public.rounds_report from anon, authenticated;
