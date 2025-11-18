from datetime import datetime
from config.database import mongo_client

db = mongo_client["zoom_attendance"]
participants = db["participants"]

async def store_zoom_event(event_data):
    event_type = event_data.get("event")
    payload = event_data.get("payload", {})
    obj = payload.get("object", {})

    meeting_id = obj.get("id")
    topic = obj.get("topic")
    participant = obj.get("participant", {})

    user_id = participant.get("user_id")
    user_name = participant.get("user_name")
    join_time = participant.get("join_time")
    leave_time = participant.get("leave_time")

    if event_type == "meeting.participant_joined":
        participants.insert_one({
            "meeting_id": meeting_id,
            "topic": topic,
            "user_id": user_id,
            "user_name": user_name,
            "join_time": join_time,
            "status": "joined",
            "created_at": datetime.utcnow()
        })
        print("✔ Saved JOIN:", user_name)
        return True

    if event_type == "meeting.participant_left":
        participants.update_one(
            {"meeting_id": meeting_id, "user_id": user_id},
            {"$set": {
                "leave_time": leave_time,
                "status": "left",
                "updated_at": datetime.utcnow()
            }},
            upsert=True
        )
        print("✔ Updated LEAVE:", user_name)
        return True

    print("⚠️ Not join/leave:", event_type)
    return False
