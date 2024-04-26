package main

import (
	"fmt"
	"log"

	"github.com/caarlos0/env/v11"
)

type Config struct {
	SenderEmail   string `env:"SENDER_EMAIL"`
	EmailPassword string `env:"EMAIL_PASSWORD"`
}

var cfg *Config

func loadEnv() {
	cfg = &Config{}
	opts := env.Options{UseFieldNameByDefault: true}

	if err := env.ParseWithOptions(cfg, opts); err != nil {
		log.Fatal(err)
	}

	fmt.Printf("%+v\n", cfg)
}
