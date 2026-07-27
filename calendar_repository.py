import os
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SECRET_KEY = os.environ["SUPABASE_SECRET_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

class CalendarRepository:

    def get_all_events(self, username, mode):
        return self.get_events(username, mode)

    def get_events(self, username, mode, start_date=None, end_date=None):
        query = (
            supabase.table("calendar_events")
            .select("*")
            .eq("username", username)
            .eq("mode", mode)
        )

        if start_date is not None:
            query = query.gte("date", start_date)
        if end_date is not None:
            query = query.lte("date", end_date)

        result = query.execute()

        events = {}
        for row in result.data:
            events[row["date"]] = {
                "timeS": row["timeS"],
                "timeE": row["timeE"],
                "comment": row["comment"]
            }

        return events

    def get_events_by_users(self, usernames, mode, start_date=None, end_date=None):
        if not usernames:
            return {}

        query = (
            supabase.table("calendar_events")
            .select("*")
            .in_("username", usernames)
            .eq("mode", mode)
        )

        if start_date is not None:
            query = query.gte("date", start_date)
        if end_date is not None:
            query = query.lte("date", end_date)

        result = query.execute()

        events_by_user = {username: {} for username in usernames}
        for row in result.data:
            user = row["username"]
            if user not in events_by_user:
                events_by_user[user] = {}
            events_by_user[user][row["date"]] = {
                "timeS": row["timeS"],
                "timeE": row["timeE"],
                "comment": row["comment"]
            }

        return events_by_user

    def save_event(self, username, mode, date, timeS, timeE, comment):
        event = {
            "username": username,
            "mode": mode,
            "date": date,
            "timeS": timeS,
            "timeE": timeE,
            "comment": comment
        }

        result = (
            supabase.table("calendar_events")
            .upsert(event, on_conflict="username, mode, date")
            .execute()
        )
        return result

    def delete_event(self, username, mode, date):
        return (
            supabase.table("calendar_events")
            .delete()
            .eq("username", username)
            .eq("mode", mode)
            .eq("date", date)
            .execute()
        )

    def delete_user_events(self, username):
        return (
            supabase.table("calendar_events")
            .delete()
            .eq("username", username)
            .execute()
        )
