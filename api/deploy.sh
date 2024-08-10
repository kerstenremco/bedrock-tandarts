rm package.zip
find . | egrep "\.(py)$" | zip -@ package.zip
aws lambda update-function-code \
    --function-name bedrock-dentibot-api \
    --zip-file fileb://package.zip