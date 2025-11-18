# Why Participants Not Showing in MongoDB

## Current Status:
- ✅ Meetings are being stored (4 meetings in database)
- ❌ Participants are NOT being stored (0 participants)

## Possible Issues:

### Issue 1: Zoom Not Sending Participant Events

**Check Zoom Webhook Configuration:**
1. Go to: https://marketplace.zoom.us/
2. Your App → Event Subscriptions
3. Verify these events are selected:
   - ✅ `participant.joined`
   - ✅ `participant.left`

**If not selected:**
- Add them to your webhook subscription
- Save and wait for Zoom to send events

### Issue 2: Participant Events Not Reaching Backend

**Check Backend Terminal:**
Look for logs like:
```
📥 Received Zoom event: participant.joined
   → Handling participant.joined
   👤 Processing participant.joined event
```

**If you don't see these:**
- Participant events aren't reaching backend
- Check Lambda CloudWatch logs
- Verify API Gateway is forwarding all events

### Issue 3: Participant Event Structure Different

Zoom might send participant events in a different structure than expected.

**Check Backend Logs:**
The updated code will now log:
```
   Event data: {...}
   Participant: {...}
```

Compare with expected structure in `zoom_webhook_service.py`

### Issue 4: Silent Failures

The code might be failing silently when processing participant events.

**Solution:** I've added detailed logging - check backend terminal for errors.

## Diagnostic Steps:

### Step 1: Test Participant Events Locally

```powershell
cd backend
python test_participant_event.py
```

This will test if the code can store participants.

### Step 2: Check Backend Logs

When a participant joins a Zoom meeting, check backend terminal for:
```
📥 Received Zoom event: participant.joined
   👤 Processing participant.joined event
   ✅ Participant stored: [name]
```

### Step 3: Verify Zoom Configuration

1. Zoom Marketplace → Your App
2. Event Subscriptions
3. Verify `participant.joined` and `participant.left` are selected
4. Check webhook is Active

### Step 4: Check Lambda Logs

1. Lambda → Monitor → CloudWatch logs
2. Look for participant events being forwarded
3. Check for any errors

## Quick Fixes:

### If Events Not Selected in Zoom:
1. Add `participant.joined` and `participant.left` to webhook
2. Save
3. Join a test meeting
4. Check backend logs

### If Events Reaching But Not Storing:
1. Check backend terminal for error messages
2. Run `python test_participant_event.py` to test locally
3. Check MongoDB for any stored participants

### If No Events at All:
1. Verify Zoom webhook is Active
2. Check API Gateway URL is correct
3. Test with a real Zoom meeting (not just started/ended)

## Test Command:

```powershell
cd backend
python test_participant_event.py
```

This will test participant event handling and show if the code works.

