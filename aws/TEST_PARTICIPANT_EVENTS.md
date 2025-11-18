# Test Participant Events After Adding to Zoom

## ✅ What You Did:
Added `participant.joined` and `participant.left` to Zoom webhook subscription.

## 📋 How to Test:

### Step 1: Create a Test Meeting

1. **Open Zoom** (desktop or web)
2. **Create a new meeting**
3. **Start the meeting** (as host)

### Step 2: Join as Participant

**Important:** Participant events only fire when someone **actually joins** the meeting.

1. **Open Zoom on another device/account** (or use incognito browser)
2. **Join the meeting** using the meeting ID or link
3. **Wait a few seconds**

### Step 3: Check Backend Terminal

You should see in the backend terminal (running `python main.py`):
```
============================================================
🔔 WEBHOOK REQUEST RECEIVED
============================================================
📥 Received Zoom event: participant.joined
   → Handling participant.joined
   👤 Processing participant.joined event
   Meeting: [meeting_id]
   Participant: {...}
   ✅ Participant stored: [name]
============================================================
```

### Step 4: Leave the Meeting

1. **Leave the meeting** (as participant)
2. **Check backend terminal** for:
```
📥 Received Zoom event: participant.left
   → Handling participant.left
   👋 Processing participant.left event
   ✅ Participant left updated: [user_id]
```

### Step 5: Verify in MongoDB

```powershell
cd backend
python check_zoom_data.py
```

You should see:
```
👥 Participants: [number > 0]
```

## 🔍 Monitor in Real-Time:

Run this to watch for new events:
```powershell
cd backend
python monitor_zoom_events.py
```

This will show new meetings and participants as they arrive.

## ⚠️ Important Notes:

1. **Participant events only fire when:**
   - Someone actually joins (not just meeting started)
   - Someone actually leaves (not just meeting ended)

2. **You need to join from a different account/device:**
   - Host joining doesn't always trigger participant.joined
   - Join as a separate participant

3. **Check backend terminal:**
   - All events will be logged there
   - Look for `participant.joined` and `participant.left`

## Troubleshooting:

**If you don't see participant events:**

1. **Verify webhook is Active:**
   - Zoom Marketplace → Event Subscriptions
   - Check status is "Active"

2. **Check events are selected:**
   - Verify `participant.joined` is checked
   - Verify `participant.left` is checked

3. **Wait a few seconds:**
   - Events may take 5-10 seconds to arrive

4. **Check Lambda logs:**
   - Lambda → CloudWatch logs
   - Look for participant events

5. **Check backend logs:**
   - Backend terminal should show all events
   - Look for any errors

## Success Indicators:

✅ Backend terminal shows `participant.joined` events
✅ Backend terminal shows `participant.left` events  
✅ MongoDB has participants: `python check_zoom_data.py`
✅ Participants show user names and meeting IDs

