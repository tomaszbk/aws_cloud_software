FROM golang:1.22 as build

WORKDIR /app
# Copy dependencies list
COPY go.mod go.sum ./

RUN go mod download
# Build with optional lambda.norpc tag
COPY main.go config.go ./

RUN go build -tags lambda.norpc -o main main.go config.go

# Copy artifacts to a clean image
FROM public.ecr.aws/lambda/provided:al2023

COPY --from=build /app/main ./main

ENTRYPOINT [ "./main" ]