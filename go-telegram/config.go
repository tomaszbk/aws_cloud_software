package main

import (
	"github.com/caarlos0/env/v11"
)

type Config struct {
	TelegramBotToken string `env:"TELEGRAM_BOT_TOKEN"`
}

var cfg *Config

func LoadConfig() (*Config, error) {
	cfg = &Config{}
	if err := env.Parse(cfg); err != nil {
		return nil, err
	}
	return cfg, nil
}
