package main

import (
	"github.com/gin-gonic/gin"
	"github.com/twilio/twilio-go"
	api "github.com/twilio/twilio-go/rest/api/v2010"
)

func main() {
	LoadConfig()
	router := gin.Default()

	router.POST("/whatsapp", handleWhatsAppMessage)

	router.Run(":3000")
}

func handleWhatsAppMessage(c *gin.Context) {
	from := c.PostForm("From")
	body := c.PostForm("Body")

	sendWhatsAppMessage(from, "Thanks for your message: "+body)
}

func sendWhatsAppMessage(to, body string) {
	client := twilio.NewRestClientWithParams(twilio.ClientParams{
		Username: cfg.TwillioAccountSID,
		Password: cfg.TwilioAuthToken,
	})

	params := &api.CreateMessageParams{}
	params.SetTo(to)
	params.SetFrom("whatsapp:+14155238886")
	params.SetBody(body)

	_, err := client.Api.CreateMessage(params)
	if err != nil {
		println("Error sending WhatsApp message:", err.Error())
	} else {
		println("Message sent successfully!")
	}

}
