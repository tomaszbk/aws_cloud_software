package main

import (
	"github.com/caarlos0/env/v11"
)

type Config struct {
	TwillioAccountSID string `env:"TWILIO_ACCOUNT_SID"`
	TwilioAuthToken   string `env:"TWILIO_AUTH_TOKEN"`
}

var cfg *Config

func LoadConfig() (*Config, error) {
	cfg = &Config{}
	if err := env.Parse(cfg); err != nil {
		return nil, err
	}
	return cfg, nil
}
