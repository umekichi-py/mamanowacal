import os
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SECRET_KEY = os.environ["SUPABASE_SECRET_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

class CalendarRepository:

    def get_all_events(self, username, mode):

        result = (
            supabase.table("calendar_events")
            .select("*")
            .eq("username", username)
            .eq("mode", mode)
            .execute()
        )

        events = {}

        for row in result.data:
            events[row["date"]] = {
                "timeS": row["timeS"],
                "timeE": row["timeE"],
                "comment": row["comment"]
            }

        return events

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
            .upsert(event, on_conflict=("username", "mode", "date"))
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
