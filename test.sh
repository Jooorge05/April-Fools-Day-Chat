source .env

curl -X POST \
    -H "Content-Type: application/json" \
    -H "X-Api-Key: $YOUR_API_KEY" \
    -d '{"user_input": "What is the capital of France?"}' http://localhost:5000/api/chat
 