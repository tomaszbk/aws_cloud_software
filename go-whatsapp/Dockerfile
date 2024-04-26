# Use a specific version of the official Golang Alpine image for the build stage
FROM golang:1.22.2-alpine3.19 AS builder

WORKDIR /app

COPY go.mod go.sum ./

# Download and install the Go dependencies
RUN go mod download

# Copy the rest of the application source code
COPY . .

# Build the Go application
RUN go build -o app

# Use a smaller base image for the final stage
FROM alpine:3.19

# Set the working directory in the final container
WORKDIR /app

# Copy the built application from the builder stage
COPY --from=builder /app/app .

# Set the entry point for the container
CMD ["./app"]
