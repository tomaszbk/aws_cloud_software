package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"gopkg.in/gomail.v2"
)

type RequestEvent struct {
	DestinyEmail string `json:"destiny_email"`
}

func handler(ctx context.Context, event RequestEvent) (events.APIGatewayProxyResponse, error) {
	// Create a new email message
	m := gomail.NewMessage()
	fmt.Println("Context:", ctx)
	fmt.Println("Event:", event)
	destinyEmail := event.DestinyEmail

	m.SetHeader("From", cfg.SenderEmail)
	m.SetHeader("To", destinyEmail)
	m.SetHeader("Subject", "Hello from Lambda!")
	m.SetBody("text/plain", "Email enviado con exito!! de tomas")
	// Send the email using SMTP
	fmt.Println("Sending email...")
	fmt.Println("Username:", cfg.SenderEmail)
	fmt.Println("Password:", cfg.SenderPassword)
	d := gomail.NewDialer("smtp.gmail.com", 587, cfg.SenderEmail, cfg.SenderPassword)
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
