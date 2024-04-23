package main

import (
	"fmt"
	"log"

	"github.com/caarlos0/env/v11"
)

type Config struct {
	SENDER_MAIL string
	PASSWORD    string
}

func loadEnv() {
	cfg := &Config{}
	opts := env.Options{UseFieldNameByDefault: true}

	if err := env.ParseWithOptions(cfg, opts); err != nil {
		log.Fatal(err)
	}

	fmt.Printf("%+v\n", cfg)
}
