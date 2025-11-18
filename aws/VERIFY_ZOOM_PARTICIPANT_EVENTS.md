# Why Participants Not Showing - Solution

## ✅ Good News:
The code WORKS! Test confirmed participants can be stored.

## ❌ The Problem:
Real Zoom meetings have 0 participants because **participant events aren't being sent by Zoom**.

## 🔍 Check Zoom Webhook Configuration:

### Step 1: Verify Event Subscriptions

1. Go to: **https://marketplace.zoom.us/**
2. Your App → **Event Subscriptions**
3. Check your webhook subscription
4. **Verify these events are selected:**
   - ✅ `participant.joined`
   - ✅ `participant.left`

**If NOT selected:**
- Click "Edit" on your webhook
- Add `participant.joined` and `participant.left`
- Save

### Step 2: Test with Real Meeting

**Important:** Participant events only fire when:
- Someone **actually joins** a meeting
- Someone **actually leaves** a meeting

**To test:**
1. Create a Zoom meeting
2. **Start the meeting** (as host)
3. **Join from another device/account** (as participant)
4. **Leave the meeting** (as participant)
5. Check backend terminal for:
   ```
   📥 Received Zoom event: participant.joined
   👤 Processing participant.joined event
   ✅ Participant stored: [name]
   ```

### Step 3: Check Backend Logs

When someone joins a meeting, you should see in backend terminal:
```
📥 Received Zoom event: participant.joined
   → Handling participant.joined
   👤 Processing participant.joined event
   Meeting: [meeting_id]
   Participant: {...}
   ✅ Participant stored: [name]
```

**If you don't see this:**
- Participant events aren't reaching backend
- Check Zoom webhook configuration
- Verify events are selected

### Step 4: Check Lambda Logs

1. Lambda → Monitor → CloudWatch logs
2. Look for `participant.joined` or `participant.left` events
3. If you see them, they're being forwarded
4. If not, Zoom isn't sending them

## Common Issues:

### Issue 1: Events Not Selected in Zoom
**Solution:** Add `participant.joined` and `participant.left` to webhook subscription

### Issue 2: No One Actually Joined
**Solution:** Make sure someone actually joins the meeting (not just started)

### Issue 3: Webhook Not Active
**Solution:** Verify webhook status is "Active" in Zoom

### Issue 4: Events Sent But Not Reaching
**Solution:** Check Lambda logs to see if events are being forwarded

## Quick Test:

1. **Verify Zoom webhook has participant events selected**
2. **Create a test meeting**
3. **Join from another device/account**
4. **Check backend terminal for participant logs**
5. **Check MongoDB:** `python check_zoom_data.py`

## What You Should See:

**In Backend Terminal:**
```
📥 Received Zoom event: participant.joined
   👤 Processing participant.joined event
   ✅ Participant stored: John Doe
```

**In MongoDB:**
```
👥 Participants: [number > 0]
```

## Next Steps:

1. ✅ Check Zoom webhook configuration
2. ✅ Add participant events if missing
3. ✅ Test with real meeting (join as participant)
4. ✅ Check backend logs
5. ✅ Verify MongoDB has participants

