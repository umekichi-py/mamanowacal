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