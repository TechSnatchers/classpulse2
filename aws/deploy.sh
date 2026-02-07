#!/bin/bash
# Deployment script for Zoom webhook AWS infrastructure

set -e

echo "🚀 Deploying Zoom Webhook Infrastructure to AWS..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if SAM CLI is installed (for Lambda deployment)
if ! command -v sam &> /dev/null; then
    echo "⚠️  SAM CLI not found. Using CloudFormation instead..."
    USE_SAM=false
else
    USE_SAM=true
fi

# Get parameters
read -p "Enter your backend API URL: " BACKEND_API_URL
read -p "Enter Zoom webhook secret token: " -s ZOOM_SECRET
echo ""

# Deploy using CloudFormation
STACK_NAME="zoom-webhook-stack"
REGION="${AWS_REGION:-us-east-1}"

echo "📦 Creating CloudFormation stack..."

aws cloudformation create-stack \
    --stack-name $STACK_NAME \
    --template-body file://cloudformation/zoom-webhook-stack.yaml \
    --parameters \
        ParameterKey=BackendApiUrl,ParameterValue=$BACKEND_API_URL \
        ParameterKey=ZoomWebhookSecretToken,ParameterValue=$ZOOM_SECRET \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION

echo "⏳ Waiting for stack creation..."
aws cloudformation wait stack-create-complete \
    --stack-name $STACK_NAME \
    --region $REGION

# Get webhook URL
WEBHOOK_URL=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`WebhookUrl`].OutputValue' \
    --output text)

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Webhook URL: $WEBHOOK_URL"
echo ""
echo "🔗 Use this URL in your Zoom app webhook configuration:"
echo "   $WEBHOOK_URL"
echo ""

