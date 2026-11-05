FROM golang:1.27 AS build
WORKDIR /src
COPY main.go .
RUN CGO_ENABLED=0 go build -o /hello main.go

FROM alpine:3.24
RUN adduser -D -u 10001 app
USER app
COPY --from=build /hello /hello
CMD ["/hello"]
