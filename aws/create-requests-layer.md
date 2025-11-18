# Create Lambda Layer with Requests Library

## Quick Method: Use Public Layer (Easiest)

Instead of creating your own, you can use a public layer that already has `requests`:

**ARN for Python 3.11 (eu-north-1):**
```
arn:aws:lambda:eu-north-1:336392948345:layer:AWSSDKPandas-Python311:2
```

Or search for "requests" layers in the AWS Layer repository.

## Method 2: Create Your Own Layer

### Step 1: Create Layer Locally

```powershell
# Create directory structure
mkdir python
cd python
pip install requests -t .

# Go back and create ZIP
cd ..
Compress-Archive -Path python -DestinationPath requests-layer.zip
```

### Step 2: Upload to Lambda

1. Go to Lambda → Layers → Create layer
2. Upload the ZIP file
3. Note the Layer ARN

### Step 3: Add to Function

1. Go back to your function
2. Add layer using the ARN you created

## Method 3: Bundle with Code (Simplest for Now)

Instead of using a layer, you can include `requests` directly in your deployment package.

1. In Lambda code editor, the dependencies you see (pymongo, etc.) suggest you might already have a package
2. You can add `requests` to that package

## Recommended: Use Public Layer

Go back to "Add layer" and choose "Specify an ARN", then use a public layer ARN for requests.

