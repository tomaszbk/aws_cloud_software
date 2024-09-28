package main

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"os/signal"

	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"
)

type User struct {
	PhoneNumber string `json:"phone_number"`
	Name        string `json:"name"`
	LastName    string `json:"last_name"`
	Email       string `json:"email"`
}

func main() {
	LoadConfig()
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt)
	defer cancel()

	opts := []bot.Option{
		bot.WithDefaultHandler(handler),
	}

	b, err := bot.New(cfg.TelegramBotToken, opts...)
	if err != nil {
		panic(err)
	}

	b.Start(ctx)
}

func handler(ctx context.Context, b *bot.Bot, update *models.Update) {

	queryParams := url.Values{}
	queryParams.Add("user_prompt", update.Message.Text)
	queryParams.Add("thread_id", fmt.Sprintf("%d", update.Message.Chat.ID))

	fullURL := fmt.Sprintf("http://%s:%s/user-message?%s", cfg.BackendHost, cfg.BackendPort, queryParams.Encode())

	// Create a new POST request
	req, err := http.NewRequest("POST", fullURL, bytes.NewBuffer([]byte{}))
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}
	// Set the content type to application/json
	req.Header.Set("Content-Type", "application/json")

	// Send the request using http.DefaultClient
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Println("Error sending POST request:", err)
		return
	}
	defer resp.Body.Close()

	// Check the response status code
	if resp.StatusCode == http.StatusOK {
		fmt.Println("POST request successful!")
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			fmt.Println("Error reading response body:", err)
			return
		}
		b.SendMessage(ctx, &bot.SendMessageParams{
			ChatID: update.Message.Chat.ID,
			Text:   string(body),
		})
	} else {
		fmt.Println("POST request failed with status:", resp.Status)
	}
}
