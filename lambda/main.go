package main

import (
	"context"
	"log"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"gopkg.in/gomail.v2"
)

func handler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	// Create a new email message
	m := gomail.NewMessage()

	m.SetHeader("From", cfg.SenderEmail)
	m.SetHeader("To", "recipient@example.com")
	m.SetHeader("Subject", "Hello from Lambda!")
	m.SetBody("text/plain", "This is the email body.")

	// Send the email using SMTP
	d := gomail.NewDialer("smtp.example.com", 587, cfg.SenderEmail, cfg.EmailPassword)
	if err := d.DialAndSend(m); err != nil {
		log.Println("Failed to send email:", err)
		return events.APIGatewayProxyResponse{}, err
	}

	response := events.APIGatewayProxyResponse{
		StatusCode: 200,
		Body:       "\"Email sent!\"",
	}
	return response, nil
}

func main() {
	loadEnv()
	lambda.Start(handler)
}
